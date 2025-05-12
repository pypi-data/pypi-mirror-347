from typing import Optional, List
from anndata import AnnData
import polars as pl
from plotly import graph_objects as go
from sclive.dataio.get_metas_func import get_metas
from sclive.dataio.get_gene_exprs_func import get_gene_exprs
from ._layout_funcs import set_2d_layout

def heatmap_plt(adata: AnnData, 
                meta_id:str, 
                gene_list:List[str],
                use_raw:Optional[bool]=False,
                layer:Optional[str]=None,
                meta_order:Optional[List[str]]=None,
                gene_order:Optional[List[str]]=None,
                ticks_font_size:Optional[int]=12,
                width:Optional[int|str]="auto", 
                height:Optional[int|str]="auto", 
                legend_font_size: Optional[int] = None,
                legend_title: Optional[str] = None,
                title_size:Optional[int]=None,
                title:Optional[str]=None,
                scale_features:Optional[bool] = False, 
                cont_color: Optional[str] = "reds",
                axis_font_size: Optional[int] = None,
                axis_labels: Optional[List[str]] = None)-> go.Figure:
  '''
  Draws co-expression scatter plot for given genes using given anndata object. This function is a wrapper for dash-bio's Clustergram function and it provide further customization options.
  
  :param adata: 
    single cell object to be plotted 
  :param meta_id: 
    adata.obs column to plot heatmap over
  :param gene_list: 
    list of genes to plot heatmap over
  :param use_raw: 
    either to use raw gene counts
  :param layer: 
    which layer to extract the gene expressions
  :param meta_order:
    order of the meta categories. If None, the order will be random
  :param gene_order:
    order of the genes. If None, the order will be random
  :param ticks_font_size: 
    size of tick labels on x and y axis 
  :param width: 
    width of the plot. Can be auto or any value Plotly graph objects accepts
  :param height: 
    height of the plot. Can be auto or 'true_asp_ratio' or any value Plotly graph objects accepts. If set to true_asp_ratio, width must be explicit and height will be set using min/max values of dimention reduction axis values
  :param legend_font_size:
    font size of the legend for mean expressions. If None legend isn't drawn
  :param legend_title:
    title for legend of mean expressions
  :param title_size: 
    font size for title
  :param title: 
    title for the plot
  :param scale_features: 
    either to scale gene expressions
  :param cont_color: 
    color gradient for dots. Can be anything Plotly graph object accepts
  :param axis_font_size:
    font size for axis labels. If None axis labels will be omitted
  :param axis_labels:
    the label of the x and y axes
  :returns:
    plotly graph figure object containing heatmap of gene list over given meta id
  ''' 
  
  if legend_font_size is not None and legend_title is None:
    legend_title = "Mean Expression"
  
  plotting_data = get_metas(adata, [meta_id], cat=True).join(get_gene_exprs(adata, gene_list,use_raw=use_raw, layer=layer), on="barcode")
  dendo_mtx = plotting_data.group_by(meta_id).agg(pl.exclude(meta_id, "barcode", "gene_exprs").mean())
  if scale_features:
    dendo_mtx = dendo_mtx.with_columns(((pl.exclude(meta_id).log1p() - pl.exclude(meta_id).log1p().min()) / (pl.exclude(meta_id).log1p().max() - pl.exclude(meta_id).log1p().min())).round(4))
  
  if meta_order is not None:
    dendo_mtx = dendo_mtx.with_columns(pl.col(meta_id).cast(pl.String)).join(pl.DataFrame({meta_id:meta_order, "ind":range(len(meta_order))}), on=meta_id).sort("ind").drop("ind")
  if gene_order is not None:
     dendo_mtx = dendo_mtx.select([meta_id] + gene_order)
  fig = go.Figure(go.Heatmap(
    z = dendo_mtx.drop(meta_id).to_numpy().transpose(),
    x = dendo_mtx[meta_id].to_list(),
    y = [c for c in dendo_mtx.columns if c in gene_list],
    colorbar = dict(
      tickfont = dict(size=legend_font_size),
      title = dict(font = dict(size=legend_font_size),
                   text = legend_title)
    ),
    showscale = legend_font_size is not None,
    colorscale=cont_color))
  
  if title_size is not None and title is None:
        title = f"{meta_id} Gene Expressions Heatmap"
  if axis_font_size is not None and axis_labels is None:
        axis_labels = [meta_id, "Genes"]
  fig = set_2d_layout(fig,
                      ticks_font_size = ticks_font_size,  
                      title_size = title_size,
                      axis_labels = axis_labels,
                      axis_font_size = axis_font_size,
                      title = title,
                      width = width, 
                      height = height)
  return fig