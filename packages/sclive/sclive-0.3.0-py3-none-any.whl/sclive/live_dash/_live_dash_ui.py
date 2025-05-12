from shiny import ui
from plotly.express import colors
from shinywidgets import output_widget

def create_dash_ui(sclive_dash):
    sclive_ui =  ui.page_sidebar(
         ui.sidebar(
          ui.h3("Plot Controls"),
               ui.accordion(
                    ui.accordion_panel("Subset Cells",
                         ui.input_select("subset_cells","",
                              choices=[v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"],
                              selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_subset_meta].name),
                         ui.input_checkbox_group("subset_meta_list", "Select which cells to show", inline = True, 
                              choices = [],
                              selected = []),
                         ui.row(
                              ui.column(6,
                                   ui.input_action_button("subset_all", "Select all groups", class_="btn btn-primary"),
                              ),
                              ui.column(6,
                                   ui.input_action_button("subset_none", "Deselect all groups", class_="btn btn-primary"),
                              )
                         )
                    ),
                    ui.accordion_panel("Graphics Control",
                    ui.input_select("color_grad", "Colour (for continuous variables and gene expressions):", choices=colors.named_colorscales()),
                    ui.input_checkbox("labels", "Show cell info labels", value=False),
                    ui.panel_conditional("input.labels==1",
                         ui.input_slider(
                              "labels_size",
                              "Labels font:",
                              min=1,
                              max=36,
                              value=12,
                              step=1,
                         )
                    ),
                    ui.input_checkbox("legend", "Show legend", value=False),
                    ui.panel_conditional("input.legend==1",
                                        ui.input_slider(
                                             "legend_size",
                                             "Legend font:",
                                             min=1,
                                             max=36,
                                             value=12,
                                             step=1,
                                        )
                                   ),
                                   ui.input_slider(
                                        "pt_size",
                                        "Point size:",
                                        min=0,
                                        max=10,
                                        value=4,
                                        step=0.25,
                                   ),
                                   ui.row(
                                        ui.column(6,
                                             ui.input_checkbox("layout_box", "Two plots", value=True),
                                             ui.input_checkbox("three_d", "3D: Z-axis", False)
                                        ),
                                        ui.column(6,
                                             ui.input_checkbox("show_txt", "Show axis text", value=False),
                                             ui.panel_conditional("input.three_d==1",
                                             ui.input_checkbox("cube", "Cube", value=True)
                                             )
                                        ),
                                        ui.input_slider(
                                             "ticks_font_size",
                                             "Axis ticks font:",
                                             min=1,
                                             max=36,
                                             value=12,
                                             step=1,
                                        )
                                   ),
                                        ui.panel_conditional("input.three_d == 1",
                                        ui.input_slider(
                                             "plt_size_3d",
                                             "Plot size (3D):",
                                             min=100,
                                             max=2400,
                                             value=600,
                                             step=50,
                                        ),

                                    ),
                                    ui.panel_conditional("input.layout_box == false & input.plot3_type == \"Gene Coexpression\"",
                                        ui.row(
                                            ui.column(12,ui.input_radio_buttons(
                                                "coexp_colors",
                                                "Colors (Coexpression):",
                                                choices=["Red(Gene1); Blue(Gene2)","Orange(Gene1); Blue(Gene2)","Red(Gene1); Green(Gene2)","Green(Gene1); Blue(Gene2)"],
                                                selected="Red(Gene1); Blue(Gene2)")
                                            ), 
                                        ),
                                    ),
                                   ui.panel_conditional("input.show_txt==1",
                                        ui.input_slider(
                                             "font_size",
                                             "Axis labels font:",
                                             min=1,
                                             max=36,
                                             value=12,
                                             step=1,
                                        )
                                   )
                    ),
                    ui.accordion_panel("Plot size (2D)",
                         ui.panel_conditional("input.true_asp_ratio==0",
                              ui.input_checkbox("auto_scale_width", "Autoscale the width", True),
                         ui.panel_conditional("input.auto_scale_width ==0",
                              ui.input_slider(
                              "plt_width",
                              "Plot width:",
                              min=100,
                              max=2400,
                              value=600,
                              step=50,
                              ),
                         ),
                         
                              ui.input_slider(
                              "plt_height",
                              "Plot height:",
                              min=100,
                              max=2400,
                              value=600,
                              step=50,
                              )
                    ),
                    ui.input_checkbox("true_asp_ratio", "True aspect ratio (Dimension reduction plots)", False),
                    ui.panel_conditional("input.true_asp_ratio==1",
                        ui.input_slider(
                            "plt_size",
                            "Plot width:",
                            min=400,
                            max=2400,
                            value=600,
                            step=50,
                        ),
                    )
                    ), 
               open=False,                    
               ),
               ui.panel_conditional("input.layout_box == false & input.plot3_type == \"Gene Coexpression\"",
                                    ui.row(ui.input_slider("coexpr_granularity", "Granularity:", min=1, max=100, value=50, step=1)),
                                    ui.row(ui.column(12, output_widget("coexp_legend")))),
         open='closed', width="25%"),
     ui.page_navbar(ui.nav_panel("Cell Features",
        ui.row(
            ui.column(
                3,
                ui.row(
                    ui.column(
                        12,
                        ui.input_select(
                            "dimred",
                            "Dimension Reduction:",
                            choices=[x.name for x in sclive_dash.dimred_infos.values()],
                            selected=sclive_dash.dimred_infos[sclive_dash.ui_defaults.default_dimred].name,
                        )
                    )
                ),
            ),
        ),
        ui.panel_conditional("input.layout_box % 2 == 1",
          ui.row(
                ui.column(
                    6,
                    ui.input_select(
                                "plot1_type",
                                "Plot Type:",
                                choices=["Cell Information", "Gene Expression"],
                                selected="Cell Information",
                            ),
                    ui.row(
                        ui.column(
                            12,
                            ui.panel_conditional(
                                "input.plot1_type == \"Cell Information\"",     
                                ui.input_select(
                                    "meta1",
                                    "Meta Column:",
                                    choices=[v.name for v in sclive_dash.meta_infos.values()],
                                    selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta1].name
                                ), 
                            ),
                            ui.panel_conditional(
                                "input.plot1_type == \"Gene Expression\"",
                                ui.column(6,
                                    ui.input_selectize(
                                        "gene1", 
                                        "Gene name:", 
                                        choices=sclive_dash.adata.var_names.to_list(), 
                                        selected=sclive_dash.ui_defaults.default_gene1),
                                )
                              ),
                        ),
                    ),
                    ui.row(ui.column(12, output_widget("dimred_plot1"))),
                    style="border-right: 2px solid black"
                ),
                ui.column(
                    6,
                    ui.input_select(
                        "plot2_type",
                        "Plot Type:",
                        choices=["Cell Information", "Gene Expression"],
                        selected="Gene Expression",
                    ),
                    ui.row(
                        ui.column(
                            12,
                            ui.panel_conditional(
                                "input.plot2_type == \"Cell Information\"",     
                                ui.input_select(
                                    "meta2",
                                    "Meta Column:",
                                    choices=[v.name for v in sclive_dash.meta_infos.values()],
                                    selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta1].name
                                ), 
                            ),
                            ui.panel_conditional(
                                "input.plot2_type == \"Gene Expression\"",
                                ui.column(6,
                                    ui.input_selectize(
                                        "gene2", 
                                        "Gene name:", 
                                        choices=sclive_dash.adata.var_names.to_list(), 
                                        selected=sclive_dash.ui_defaults.default_gene1),
                                )
                              ),
                        ),
                    ),
                    ui.row(ui.column(12, output_widget("dimred_plot2"))),
                    id="gene_exprs_col"
                ),                
          ),
          ui.br(),
          ui.row(
              ui.panel_conditional(
                    "input.plot2_type != input.plot1_type",
                    ui.row(ui.input_action_button("df_toggle2", 
                                             "Toggle to show cell numbers / statistics"))                    
               )
          ),
          ui.row(
              ui.panel_conditional(
               "input.plot2_type != input.plot1_type & input.df_toggle2 % 2 == 1",                
               ui.h4("Cell numbers / statistics"),
               )
          ),
          ui.row(
               ui.panel_conditional(
                    "input.plot2_type != input.plot1_type & input.df_toggle2 % 2 == 1",                
                    ui.input_radio_buttons(
                         "df_split",
                         "Split continuous cell info into:",
                         choices=["Quartile", "Decile"],
                         selected="Decile",
                         inline=True)
                    )
          ),
          ui.row(
              ui.panel_conditional(
                    "input.plot2_type != input.plot1_type & input.df_toggle2 % 2 == 1",
                    ui.dataframe.output_data_frame("df_out")
               )
          )
        ),
        ui.panel_conditional("input.layout_box % 2 == 0", 
               ui.column(
                    12,
                    ui.input_select(
                                "plot3_type",
                                "Plot Type:",
                                choices=["Cell Information", "Gene Expression", "Gene Coexpression"],
                                selected="Cell Information",
                    ),
                    ui.row(
                        ui.column(
                            12,
                            ui.panel_conditional(
                                "input.plot3_type == \"Cell Information\"",     
                                ui.input_select(
                                    "meta3",
                                    "Meta Column:",
                                    choices=[v.name for v in sclive_dash.meta_infos.values()],
                                    selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta1].name
                                ), 
                            ),
                            ui.panel_conditional(
                              "input.plot3_type == \"Gene Expression\"",
                              ui.column(6,
                                    ui.input_selectize("gene3", 
                                                       "Gene name:", 
                                                       choices=sclive_dash.adata.var_names.to_list(), 
                                                        selected=sclive_dash.ui_defaults.default_gene1),
                                )
                              ),
                            ui.panel_conditional(
                                "input.plot3_type == \"Gene Coexpression\"",
                                ui.column(6,
                                    ui.input_selectize("gene_coex1", "First Gene Name:", choices=sclive_dash.adata.var_names.to_list(), selected=sclive_dash.ui_defaults.default_gene2),
                                    ui.input_selectize("gene_coex2", "Second Gene Name:", choices=sclive_dash.adata.var_names.to_list(), selected=sclive_dash.ui_defaults.default_gene3),
                                )
                            ),
                        ),
                    ),
                    output_widget("dimred_plot3"),
                    ui.br()
                ))
          ),
          ui.nav_panel("Box/Violin Plot",
                ui.row(ui.accordion(ui.accordion_panel("Additional Plot Options",
                    ui.row(ui.column(6,
                        ui.input_select("box_vln_input1", "Cell information (X-axis):", 
                            choices=[v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"],
                              selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta2].name),
                        ui.input_radio_buttons("box_vln_type", "Plot type:", 
                            choices = ["violin", "boxplot"], 
                            selected = "violin", inline = True),
                            ui.br(),ui.br(),
                        ui.panel_conditional("input.box_vln_type == \"violin\"",
                                            ui.input_radio_buttons("vln_type","",
                                                                    choices=["Single", "Grouped", "Split"], 
                                                                    selected="Single"), 
                        ),
                        ui.panel_conditional("input.box_vln_type == \"boxplot\"",
                                            ui.input_radio_buttons("box_type", "",
                                                                    choices=["Single", "Grouped"], 
                                                                    selected="Single")
                        ),
                        style="border-right: 2px solid black"
                ), ui.column(6, 
                            ui.input_select("box_vln_input2", "Cell Info / Gene name (Y-axis):", 
                                        choices=[k for k,v in sclive_dash.meta_infos.items() if v.meta_type=="num"]+sclive_dash.adata.var_names.to_list(),
                                        selected=sclive_dash.ui_defaults.default_gene2,
                                        selectize=True),
                            ui.input_select("box_vln_input3", "Cell information (Group by):", 
                                choices = [v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"], 
                                selected = sclive_dash.ui_defaults.default_meta3),
                            ui.input_radio_buttons("box_vln_show_pts", "Show Points:",
                                                   choices=["All points", "Outliers", "Don't show points"],
                                                    selected="Don't show points"))),
            value="plt_options"), id="box_vln_nav")),ui.br(), ui.br(),
            ui.row(
                    ui.column(12, output_widget("box_vln_plt")),
            )
        ),
        ui.nav_panel("Proportion Plot",
               ui.row(ui.accordion(ui.accordion_panel("Additional Plot Options",
                    ui.row(ui.column(6,
                                ui.input_select("propt_input1", "Cell information (X-axis):", 
                                    choices = [v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"], 
                                    selected = sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta2].name),
                                ui.input_radio_buttons("propt_plot_type", "Plot value:", 
                                    choices = ["Proportion", "Cell Numbers"], 
                                    selected = "Proportion", inline = True),
                                ui.input_checkbox("propt_stacked","Stack/Group Barplots", True),
                                ui.input_checkbox("propt_flip_coord","Flip X/Y", False),
                                style="border-right: 2px solid black"), 
                            ui.column(6, ui.input_select("propt_input2", "Cell Info / Gene name (Y-axis):", 
                                        choices=[v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"],
                                        selected=sclive_dash.meta_infos[sclive_dash.ui_defaults.default_meta3].name)))
            ,value="plt_options"), id="proportion_nav")),ui.br(), ui.br(), ui.row(ui.column(12, output_widget("propt_out"))
            )
        ),
        ui.nav_panel("Dot Plot/Heatmap",
               ui.row(ui.accordion(ui.accordion_panel("Additional Plot Options",
                    ui.row(ui.column(6,ui.input_select("dot_heat_input1", "Group by:", 
                        choices = [v.name for v in sclive_dash.meta_infos.values() if v.meta_type=="cat"], 
                        selected = sclive_dash.ui_defaults.default_meta2),
                    ui.input_radio_buttons("dot_heat_plot_type", "Plot type:", 
                            choices = ["Dot plot", "Heatmap"], 
                            selected = "Dot plot", inline = True),
                        ui.input_checkbox("stan_features", "Standardize Features", False),
                    style="border-right: 2px solid black"), 
                    ui.column(6, ui.input_text_area("dot_heat_genes", "Gene list:",height="200px", value=",\n".join(sclive_dash.ui_defaults.default_genes_list)),))
                        ,value="plt_options"), id="dot_heat_nav")),ui.br(), ui.br(), 
                ui.row(ui.column(12, output_widget("dot_heat_plot_out"))
            )
        ), id="main_nav",   
     )
    )
    return sclive_ui