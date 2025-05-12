import re
from collections import OrderedDict
import polars as pl
from shiny import ui, reactive, render
from shinywidgets import render_widget
import plotly.express as px
from sclive.dataio.get_gene_exprs_func import get_gene_exprs
from sclive.plotting import (dimred_plt_3d,
                            dimred_plt_2d,
                            heatmap_plt,
                            dot_plt,
                            prop_plt,
                            box_plt,
                            violin_plt,
                            dimred_coexprs_2d,
                            dimred_coexprs_3d)

def create_dash_server(sclive_dash):
  def server(input, output, session):
    @reactive.Calc
    def subset_data_by_barcode():
        meta_id, meta_info = [(k,v) for k,v in sclive_dash.meta_infos.items() if v.name == input.subset_cells()][0]
        if len(input.subset_meta_list()) == 0 or len(input.subset_meta_list()) == len(meta_info.vals):
          return sclive_dash.meta_data["barcode"].to_list()
        return sclive_dash.meta_data.filter(pl.col(meta_id).is_in(input.subset_meta_list()))["barcode"].to_list()
    
    @reactive.Calc
    def get_dimred():
      return [(k,v) for k,v in sclive_dash.dimred_infos.items() if v.name==input.dimred()][0]
    
    @reactive.Calc
    def get_plot_params():
        cube = "cube" if input.cube() else "data"
        if cube:
            plt_size_3d = input.plt_size_3d()
        else:
            plt_size_3d = input.plt_width_3d()
        
        if input.true_asp_ratio():
            width = input.plt_size()
            height = "true_asp_ratio"
        else:
            if input.auto_scale_width():
                width = "auto"
            else:
                width = input.plt_width()
            height = input.plt_height()
        
        if input.show_txt():
            txt_size = input.font_size()
        else:
            txt_size = None
        
        if input.labels():
            labels_size = input.labels_size()
        else:
            labels_size = None
        
        if input.legend():
            legend_font_size = input.legend_size()
        else:
            legend_font_size = None

        ticks_font_size = input.ticks_font_size()
        
        cont_color = input.color_grad()
        return (cube, 
                plt_size_3d, 
                width, 
                height, 
                ticks_font_size,
                txt_size, 
                labels_size, 
                legend_font_size, 
                cont_color)


    @reactive.Calc
    def plot_coexprs_plt():
        if input.plot3_type() != "Gene Coexpression":
           return None, None
        else:
          gene1 = input.gene_coex1()
          gene2 = input.gene_coex2()
          if gene1 == gene2 or gene1 not in sclive_dash.adata.var_names or gene2 not in sclive_dash.adata.var_names:
            return None, None
          selected_barcodes = subset_data_by_barcode()
          cube, plt_size_3d, width, height, ticks_font_size, txt_size, labels_size, legend_font_size, cont_color = get_plot_params()
          gran = input.coexpr_granularity()
          dimred = get_dimred()
          match input.coexp_colors():
              case "Red(Gene1); Blue(Gene2)":
                  color1 = [255, 0, 0]
                  color2 = [0, 0, 255]
              case "Orange(Gene1); Blue(Gene2)":
                  color1 = [255, 140, 0]
                  color2 = [0, 0, 255]
              case "Red(Gene1); Green(Gene2)":
                  color1 = [255, 0, 0]
                  color2 =[0, 255, 0]
              case "Green(Gene1); Blue(Gene2)": 
                  color1 = [0, 255, 0]
                  color2 = [0, 0, 255]
          if input.three_d():
            return dimred_coexprs_3d(
                          sclive_dash.adata,
                          dimred[0], 
                          gene1=gene1,
                          gene2=gene2, 
                          expr_color1=color1,
                          expr_color2=color2,
                          selected_barcodes=selected_barcodes, 
                          granularity=gran,
                          aspectmode=cube,
                          plt_size=plt_size_3d,
                          pt_size=input.pt_size(),
                          dimred_labels=dimred[1].labels_3d,
                          axis_font_size=txt_size,
                          ticks_font_size=ticks_font_size)
          else:
            return dimred_coexprs_2d(
                          sclive_dash.adata,
                          dimred[0], 
                          gene1 = gene1,
                          gene2=gene2, 
                          expr_color1=color1,
                          expr_color2=color2,
                          selected_barcodes=selected_barcodes,
                          granularity=gran,
                          width=width,
                          height=height,
                          pt_size=input.pt_size(),
                          dimred_labels=dimred[1].labels_2d,
                          axis_font_size=txt_size,
                          ticks_font_size=ticks_font_size)
    
    @output
    @render_widget
    def coexp_legend():
      coexp_legend = plot_coexprs_plt()[0]
      if coexp_legend is not None:
        fig = px.imshow(plot_coexprs_plt()[0])
        fig.update_xaxes(
            showticklabels=False,
        )
        fig.update_yaxes(
            showticklabels=False,
        )
        fig.update_traces(
            hoverinfo='skip', hovertemplate=None,
        )
        return fig
      else:
        return None
    

    @reactive.Effect
    @reactive.event(input.main_nav, ignore_none=True)
    def main_nav_change():
       if input.main_nav() != "Cell Features":
          ui.update_checkbox("true_asp_ratio", value=False)
    

    @reactive.Effect(priority=100)
    @reactive.event(input.subset_cells, ignore_none=True)
    def subset_meta_cats(): 
      meta = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.subset_cells()][0]
      ui.update_checkbox_group("subset_meta_list", inline=True,
                              choices = sclive_dash.meta_infos[meta].vals,
                              selected = sclive_dash.meta_infos[meta].vals
      )
    
    @reactive.Effect
    @reactive.event(input.subset_all, ignore_none=True)
    def all_celltypes_selected():
      meta = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.subset_cells()][0]
      ui.update_checkbox_group("subset_meta_list",
                              selected=sclive_dash.meta_infos[meta].vals)

    @reactive.Effect
    @reactive.event(input.subset_none, ignore_none=True)
    def no_celltypes_selected():
      ui.update_checkbox_group("subset_meta_list", selected=[])
    
    @reactive.Effect
    @reactive.event(input.plot1_type, ignore_none=True)
    def update_gene1():
      gene = input.gene1()
      ui.update_selectize("gene1",
                              choices = list(sclive_dash.adata.var_names),
                              selected=gene 
      )

    @reactive.Effect
    @reactive.event(input.plot1_type, ignore_none=True)
    def update_gene2():
      gene = input.gene2()
      ui.update_selectize("gene2",
                              choices = list(sclive_dash.adata.var_names),
                              selected=gene 
      )

    @reactive.Effect
    @reactive.event(input.plot1_type, ignore_none=True)
    def update_gene3():
      gene = input.gene3()
      ui.update_selectize("gene3",
                              choices = list(sclive_dash.adata.var_names),
                              selected=gene 
      )
    
    @output
    @render_widget
    def dimred_plot1():
      selected_barcodes = subset_data_by_barcode()
      cube, plt_size_3d, width, height, ticks_font_size, txt_size, labels_size, legend_font_size, cont_color = get_plot_params()
      dimred = get_dimred()
      meta1 = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.meta1()][0]
      gene1 = input.gene1()
      if meta1 not in sclive_dash.adata.obs.columns or gene1 not in sclive_dash.adata.var_names:
        return None
      if input.plot1_type()=="Cell Information" and sclive_dash.meta_infos[meta1].meta_type == "cat":
        meta_order = sclive_dash.meta_infos[meta1].vals
      else:
        meta_order = "increasing"
      if input.three_d():
        return dimred_plt_3d(sclive_dash.adata, 
                              dimred_id=dimred[0],
                              meta_id= gene1 if input.plot1_type()=="Gene Expression" else meta1,
                              is_gene_exp=input.plot1_type()=="Gene Expression",
                              meta_order=meta_order,
                              cont_color=cont_color,
                              selected_barcodes=selected_barcodes,
                              labels_size=labels_size,
                              legend_font_size=legend_font_size,
                              aspectmode=cube,
                              plt_size=plt_size_3d,
                              pt_size=input.pt_size(),
                              dimred_labels=dimred[1].labels_3d,
                              axis_font_size=txt_size,
                              ticks_font_size=ticks_font_size)
      else:
        return dimred_plt_2d(sclive_dash.adata, 
                              dimred_id = dimred[0], 
                              meta_id=gene1 if input.plot1_type()=="Gene Expression" else meta1,
                              is_gene_exp=input.plot1_type()=="Gene Expression",
                              meta_order=meta_order,
                              cont_color=input.color_grad(),
                              selected_barcodes=selected_barcodes,
                              labels_size=labels_size,
                              legend_font_size=legend_font_size,
                              width=width,
                              height=height,
                              pt_size=input.pt_size(),
                              dimred_labels=dimred[1].labels_2d,
                              axis_font_size=txt_size,
                              ticks_font_size=ticks_font_size)
    
    @output
    @render_widget
    def dimred_plot2():
      selected_barcodes = subset_data_by_barcode()
      cube, plt_size_3d, width, height, ticks_font_size, txt_size, labels_size, legend_font_size, cont_color = get_plot_params()
      dimred = get_dimred()
      meta2 = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.meta2()][0]
      gene2 = input.gene2()
      if meta2 not in sclive_dash.adata.obs.columns or gene2 not in sclive_dash.adata.var_names:
        return None
      if input.plot2_type()=="Cell Information" and sclive_dash.meta_infos[meta2].meta_type == "cat":
        meta_order = sclive_dash.sclive_dash_config["meta_info"][meta2]["vals"]
      else:
        meta_order = "increasing"
      if input.three_d():
        return dimred_plt_3d(sclive_dash.adata, 
                              dimred_id=dimred[0],
                              meta_id=gene2 if input.plot2_type()=="Gene Expression" else meta2,
                              is_gene_exp=input.plot2_type()=="Gene Expression",
                              meta_order=meta_order,
                              cont_color=cont_color,
                              selected_barcodes=selected_barcodes,
                              labels_size=labels_size,
                              legend_font_size=legend_font_size,
                              aspectmode=cube,
                              plt_size=plt_size_3d,
                              pt_size=input.pt_size(),
                              dimred_labels=dimred[1].labels_3d,
                              axis_font_size=txt_size,
                              ticks_font_size=ticks_font_size)
      else:
        return dimred_plt_2d(sclive_dash.adata, 
                              dimred_id = dimred[0], 
                              meta_id=gene2 if input.plot2_type()=="Gene Expression" else meta2,
                              is_gene_exp=input.plot2_type()=="Gene Expression",
                              meta_order=meta_order,
                              cont_color=cont_color,
                              selected_barcodes=selected_barcodes,
                              labels_size=labels_size,
                              legend_font_size=legend_font_size,
                              width=width,
                              height=height,
                              pt_size=input.pt_size(),
                              dimred_labels=dimred[1].labels_2d,
                              axis_font_size=txt_size,
                              ticks_font_size=ticks_font_size)
        
    @output
    @render_widget
    def dimred_plot3():
      selected_barcodes = subset_data_by_barcode()
      cube, plt_size_3d, width, height, ticks_font_size, txt_size, labels_size, legend_font_size, cont_color = get_plot_params()
      dimred = get_dimred()
      meta3 = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.meta3()][0]
      gene3 = input.gene1()
      if meta3 not in sclive_dash.adata.obs.columns or gene3 not in sclive_dash.adata.var_names:
        return None
      if input.plot3_type()=="Cell Information" and sclive_dash.meta_infos[meta3].meta_type == "cat":
        meta_order = sclive_dash.meta_infos[meta3].vals
      else:
        meta_order = "increasing"
      if input.plot3_type() == "Gene Coexpression":
        return plot_coexprs_plt()[1]
      else:
        if input.three_d():
          return dimred_plt_3d(sclive_dash.adata, 
                                dimred_id=dimred[0],
                                meta_id=gene3 if input.plot3_type()=="Gene Expression" else meta3,
                                is_gene_exp=input.plot3_type()=="Gene Expression",
                                cont_color=cont_color,
                                selected_barcodes=selected_barcodes,
                                meta_order=meta_order,
                                labels_size=labels_size,
                                legend_font_size=legend_font_size,
                                aspectmode=cube,
                                plt_size=plt_size_3d,
                                pt_size=input.pt_size(),
                                dimred_labels=dimred[1].labels_3d,
                                axis_font_size=txt_size,
                                ticks_font_size=ticks_font_size)
        else:
          return dimred_plt_2d(sclive_dash.adata, 
                                dimred_id = dimred[0], 
                                meta_id=gene3 if input.plot3_type()=="Gene Expression" else meta3,
                                is_gene_exp=input.plot3_type()=="Gene Expression",
                                meta_order=meta_order,
                                cont_color=cont_color,
                                selected_barcodes=selected_barcodes,
                                labels_size=labels_size,
                                legend_font_size=legend_font_size,
                                width=width,
                                height=height,
                                pt_size=input.pt_size(),
                                dimred_labels=dimred[1].labels_2d,
                                axis_font_size=txt_size,
                                ticks_font_size=ticks_font_size)
    
    @render.data_frame
    def df_out():
      if input.plot1_type() == input.plot2_type():
        return pl.DataFrame()
      else:
        if input.plot1_type() == "Cell Information":
          meta = input.meta1()
          gene = input.gene2()
        else:
          meta = input.meta2()
          gene = input.gene1()
      meta, typ = [(k, v.meta_type) for k,v in sclive_dash.meta_infos.items() if v.name == meta][0]
      selected_data = sclive_dash.meta_data.filter(pl.col("barcode").is_in(subset_data_by_barcode()))
      if typ == "num":
        if input.df_split() == "Quartile":
          meta_df = selected_data.with_columns(pl.col(meta).qcut([0.25,0.5,0.75], labels=["<%25","<%50","%75","<%100"], include_breaks=True))
        else:
          meta_df = selected_data.with_columns(pl.col(meta).qcut([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], labels=["<%10", "<%20", "<%30", "<%40", "<%50", "<%60", "<%70", "<%80", "<%90", "<%100"], include_breaks=True))
        cell_info = (meta_df.group_by(meta).len(name="count")
                     .join(
                       get_gene_exprs(sclive_dash.adata, [gene],use_raw=True).join(meta_df, on = "barcode").filter(pl.col(gene)>0).group_by(meta).len(name="expressed"),
                       on=meta)
                     .with_columns(percentage = (pl.col("expressed")/pl.col("count")*100).round(2))).unnest(meta).with_columns(pl.col("breakpoint").round(2)).rename({"category":"break", "breakpoint":"Upper bound"})
      elif typ == "cat":
        cell_info = (selected_data.group_by(meta).len(name="count")
                   .join(
                     get_gene_exprs(sclive_dash.adata, [gene],use_raw=True).join(selected_data, on = "barcode").filter(pl.col(gene)>0).group_by(meta).len(name="expressed"),
                     on=meta)
                   .with_columns(percentage = (pl.col("expressed")/pl.col("count")*100).round(2)))
      return cell_info
    
    @output
    @render_widget
    def dot_heat_plot_out():
        meta_id = [k for k,v in sclive_dash.meta_infos.items() if v.name == input.dot_heat_input1()][0]
        selected_barcodes = subset_data_by_barcode()
        adata = sclive_dash.adata[selected_barcodes, :]
        gene_list = reversed(list(OrderedDict.fromkeys([gene for gene in map(lambda x: x.strip().upper(),re.split(r',|\n|,\n', input.dot_heat_genes())) if gene !=''])))
        gene_list = list(filter(lambda x: x in list(adata.var_names), gene_list))
        if len(gene_list)<2:
          return None
        
        _, _, width, height, ticks_font_size, txt_size, _, legend_font_size, cont_color = get_plot_params()
        if height == "true_asp_ratio":
            height = width

        if input.dot_heat_plot_type()=="Heatmap":
          return heatmap_plt(adata, 
                                meta_id=meta_id,
                                gene_list = gene_list,
                                axis_font_size=txt_size,
                                meta_order=sclive_dash.meta_infos[meta_id].vals,
                                gene_order=gene_list,
                                width=width,
                                height=height,
                                legend_font_size=legend_font_size,
                                ticks_font_size=ticks_font_size,
                                scale_features=input.stan_features(),
                                cont_color=cont_color)
        else:
          return dot_plt(adata, 
                            meta_id=meta_id,
                            gene_list = gene_list,
                            meta_order=sclive_dash.meta_infos[meta_id].vals,
                            gene_order=gene_list,    
                            axis_font_size=txt_size,
                            ticks_font_size=ticks_font_size,
                            width=width,
                            height=height,
                            legend_font_size=legend_font_size,
                            scale_features=input.stan_features(),
                            cont_color=cont_color)
    
    @output
    @render_widget
    def propt_out():
        selected_barcodes = subset_data_by_barcode()
        adata = sclive_dash.adata[selected_barcodes, :]
        meta_id1, meta_value1 = [(k,v) for k,v in sclive_dash.meta_infos.items() if v.name == input.propt_input1()][0]
        meta_id2, meta_value2 = [(k,v) for k,v in sclive_dash.meta_infos.items() if v.name == input.propt_input2()][0]
        _, _, width, height, ticks_font_size, axis_font_size, _, _, _ = get_plot_params()
        if height == "true_asp_ratio":
            height = width
                
        if meta_id1 == meta_id2 or meta_value1.meta_type != "cat" or meta_value2.meta_type != "cat":
            m = ui.modal(
                "Please select two separate category meta columns to see relative proportions...",
                title="Incompatible grouping variables",
                easy_close=True,
                footer=None,
            )
            ui.modal_show(m)
            return None
        else:
            return prop_plt(
                    adata,
                    x = meta_id1,
                    y = meta_id2,
                    x_order = sclive_dash.meta_infos[meta_id1].vals,
                    group_order = sclive_dash.meta_infos[meta_id2].vals,
                    axis_labels=[meta_value1.name, meta_value2.name],
                    stacked = input.propt_stacked(),
                    plt_type = "pct" if input.propt_plot_type() == "Proportion" else "count",
                    coord_flip = input.propt_flip_coord(),
                    axis_font_size = axis_font_size,
                    ticks_font_size = ticks_font_size,
                    width = width,
                    height = height
                )
    @output
    @render_widget
    def box_vln_plt():
        selected_barcodes = subset_data_by_barcode()
        adata = sclive_dash.adata[selected_barcodes, :]
        _, _, width, height, ticks_font_size, txt_size, _, legend_font_size, _ = get_plot_params()
        if height == "true_asp_ratio":
            height = width
        meta_id1, meta_value1 = [(k,v) for k,v in sclive_dash.meta_infos.items() if v.name == input.box_vln_input1()][0]
        meta_id3, meta_value3 = [(k,v) for k,v in sclive_dash.meta_infos.items() if v.name == input.box_vln_input3()][0]
        
        meta_id2 = input.box_vln_input2()
        try:
           meta2_name = sclive_dash.meta_infos[meta_id2].name
        except KeyError:
           meta2_name = meta_id2
        
        plt_type = input.box_vln_type()
        plt_type = "vln" if plt_type == "violin" else "box"
        
        vln_type = input.vln_type()
        vln_type = "single" if vln_type == "Single" else "grouped" if vln_type=="Grouped" else "split"
        
        box_type = input.box_type()
        box_type = "single" if box_type == "Single" else "grouped"
        
        pts = input.box_vln_show_pts()
        pts = "all" if pts == "All points" else "outliers" if pts=="Outliers" else False
        
        if (plt_type == "vln") and vln_type=="split" and len(meta_value3.vals) != 2:
          m = ui.modal(
              "Split violin plots are only available for grouping variables with two levels...",
              title="Incompatible grouping variables",
              easy_close=True,
              footer=None,
          )
          ui.modal_show(m)
          return None
        else:
          if plt_type == "vln":
             return violin_plt(adata,
                              x_var = meta_id1,
                              meta_id = meta_id2,
                              group_by = meta_id3,
                              x_order = sclive_dash.meta_infos[meta_id1].vals,
                              group_order = sclive_dash.meta_infos[meta_id3].vals,
                              pts=pts,
                              vln_type=vln_type,
                              pt_size=input.pt_size(),
                              legend_font_size=legend_font_size,
                              ticks_font_size=ticks_font_size,
                              axis_font_size=txt_size,
                              width=width,
                              height=height,
                              axis_labels=[meta_value1.name, meta2_name])
          else:
             return box_plt(adata,
                            x_var = meta_id1,
                            meta_id = meta_id2,
                            group_by = meta_id3,
                            x_order = sclive_dash.meta_infos[meta_id1].vals,
                            group_order = sclive_dash.meta_infos[meta_id3].vals,
                            pts=pts,
                            box_type=box_type,
                            pt_size=input.pt_size(),
                            legend_font_size=legend_font_size,
                            ticks_font_size=ticks_font_size,
                            axis_font_size=txt_size,
                            width=width,
                            height=height,
                            axis_labels=[meta_value1.name, meta2_name])
  return server