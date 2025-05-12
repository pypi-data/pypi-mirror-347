from dataclasses import dataclass
from collections import OrderedDict
from typing import List, Optional
from distinctipy import get_colors, get_hex
from random import sample
import polars as pl
import polars.selectors as cs
from anndata import AnnData
@dataclass
class MetaInfo:
    """
    MetaInfo is a class that contains information about a meta variable to use in live dash app
    It contains the following attributes:
    - meta_type:
        - "cat": categorical variable
        - "num": numerical variable
    - vals:
        - List of values for the meta variable. This attribute also determines the order of the values for this meta info
    - colors: List[str]
        - List of colors for the meta variable for each value in vals
    - name: str
        - Name of the meta variable to be used on UI
    """
    meta_type: str
    vals: List[str]
    colors: List[str]
    name: str

@dataclass
class DimredInfo:
    """
    DimredInfo is a class that contains information about a dimensionality reduction variable.
    It contains the following attributes:
    - name:
        - Name of the dimensionality reduction variable to be used on UI
    - labels_2d:
        - labels for axes for any 2D plot this dimred variable will be used in
    - labels_3d: List[str]
        - labels for axes for any 3D plot this dimred variable will be used in
    - comps_2d: List[int]
        - which components to use for 2D plots using this dimred variable
    - comps_3d: List[int]
        - which components to use for 3D plots using this dimred variable
    """
    name: str
    labels_2d: List[str]
    labels_3d: List[str]
    comps_2d: List[int]
    comps_3d: List[int]

@dataclass
class UIDefaults:
    """
    UIDefaults is a class that contains the default values for the UI.
    It contains the following attributes:
    - default_subset_meta: str
    - default_meta1: str
    - default_meta2: str
    - default_meta3: str
    - default_dimred: str
    - default_gene1: str
    - default_gene2: str
    - default_gene3: str
    - default_genes_list: List[str]
    """
    default_subset_meta: str
    default_meta1: str
    default_meta2: str
    default_meta3: str
    default_dimred: str
    default_gene1: str
    default_gene2: str
    default_gene3: str
    default_genes_list: List[str]


class ScLiveDash:
    def __init__(self, 
                 adata: AnnData, 
                 meta_ids:Optional[List[str]]=None,
                 meta_infos:Optional[OrderedDict]=None,
                 metas_schema:Optional[OrderedDict]=None,
                 dimred_ids:Optional[List[str]]=None,
                 default_dimred: Optional[str]=None, 
                 default_subset_meta=None,
                 default_meta1: Optional[str]=None, 
                 default_meta2: Optional[str]=None, 
                 default_meta3: Optional[str]=None, 
                 default_gene1: Optional[str]=None, 
                 default_gene2: Optional[str]=None, 
                 default_gene3: Optional[str]=None, 
                 meta_colors:Optional[OrderedDict]=None,
                 meta_vals:Optional[OrderedDict]=None,
                 meta_names:Optional[OrderedDict]=None,
                 dimred_infos:Optional[OrderedDict]=None,
                 dimred_labels_2d:Optional[OrderedDict] = None,
                 dimred_labels_3d:Optional[OrderedDict] = None,
                 dimred_comps_2d:Optional[OrderedDict] = None,
                 dimred_comps_3d:Optional[OrderedDict]= None,
                 dimred_names:Optional[OrderedDict] = None,
                 default_genes_list:Optional[List[str]]=None):
        """
        ScLiveDash is a class that creates a dashboard for visualizing single-cell data.
        It takes an AnnData object and creates a dashboard with various options for visualization.
        
        :param adata: 
            AnnData object containing the single-cell data to build the dashboard
        :param meta_ids: 
            List of meta ids to be used in the dashboard. If None, all meta ids in adata.obs will be used
        :param meta_infos: 
            Dictionary of meta ids and their corresponding MetaInfo objects. Any given MetaInfo object will override the default values for that meta id
        :param metas_schema: 
            Dictionary of meta ids and their corresponding type. If None, all types will be inferred from the adata.obs dataframe
        :param dimred_ids: 
            List of dimred ids to be used in the dashboard. If None, all dimred ids in adata.obsm will be used
        :param default_dimred: 
            Default dimred id to be used in the dashboard
        :param default_subset_meta: 
            Default meta id to be used in subset dropdown. If None, a random subset meta id will be used
        :param default_meta1: 
            This meta id is used for cell information default in cell information tab. If None, a random meta id will be used
        :param default_meta2: 
            This meta id is used for x axis variable for proportion plot, box plot, violin plot, heatmap and dotplot. If None, a random meta id will be used
        :param default_meta3: 
           This meta id is used for y axis of propotion plot and grouping variable of violin adn box plot. If None, a random meta id will be used
        :param default_gene1: 
            Default gene to be used in gene expression plots in cell information tab. If None, a random gene will be used.
        :param default_gene2: 
            Default gene to be used in violin plot and box plot and first gene of coexpression plot. If None, a random gene will be used.
        :param default_gene3: 
            Default gene to be used as the second gene in coexpression plot. If None, a random gene will be used.
        :param meta_colors: 
            Dictionary of meta ids and their corresponding colors for each values. If None, colors will be generated automatically.
        :param meta_vals: 
            Dictionary of meta ids and their corresponding values. This also determines the order of meta values. If None, values will be generated automatically
        :param meta_names: 
            Dictionary of meta ids and their corresponding names. If None, names will be upper cases of the meta id
        :param dimred_infos: 
            Dictionary of dimred ids and their corresponding DimredInfo objects. Any given DimredInfo object will override the default values for that dimred id
        :param dimred_labels_2d: 
            Dictionary of dimred ids and their corresponding 2D labels. If None, labels will be generated name_{i} for i corresponds to dimred component index.
        :param dimred_labels_3d: 
            Dictionary of dimred ids and their corresponding 3D labels. If None, labels will be generated name_{i} for i corresponds to dimred component index
        :param dimred_comps_2d: 
            Dictionary of dimred ids and their corresponding 2D components. If None, 0 and 1 will be used
        :param dimred_comps_3d:
            Dictionary of dimred ids and their corresponding 3D components. If None, 0, 1 and 2 will be used
        :param dimred_names: 
            Dictionary of dimred ids and their corresponding names. If None, names will be upper cases of the dimred id
        :param default_genes_list: 
            Default list of genes to be used in heatmap and dotplot. If None, a random list of genes 10 will be used
        """
        
        self.adata = adata
        self.meta_data = pl.from_pandas(adata.obs.reset_index()).rename({"index":"barcode"})
        self.meta_infos = OrderedDict()

        if meta_infos is None:
            meta_infos = OrderedDict()
        if metas_schema is None:
            metas_schema = OrderedDict()
        if meta_colors is None:
            meta_colors = OrderedDict()
        if meta_vals is None:
            meta_vals = OrderedDict()
        if meta_names is None:
            meta_names = OrderedDict()
        
        if meta_ids is None:
            meta_ids = self.meta_data.drop("barcode").columns
        
        for meta in meta_ids:
            if meta in meta_infos.keys():
                self.meta_infos[meta] = meta_infos[meta]
            else:
                self.add_meta(meta_id=meta,
                              meta_name=meta_names.get(meta, None),
                              meta_type=metas_schema.get(meta, None),
                              meta_vals=meta_vals.get(meta, None),
                              meta_colors=meta_colors.get(meta, None))
        
        if dimred_ids is None:
            self.dimred_infos = OrderedDict.fromkeys(self.adata.obsm.keys())
        else:
            self.dimred_infos = OrderedDict.fromkeys(dimred_ids)

        for dr in self.dimred_infos.keys():
            if dimred_infos and dr in dimred_infos.keys():
                self.dimred_infos[dr] = meta_infos[dr]
            else:
                if dimred_names and dr in dimred_names.keys():
                    name = dimred_names[dr]
                else:
                    name = dr.upper()
                
                if dimred_comps_2d and dr in dimred_comps_2d.keys():
                    comps_2d = dimred_comps_2d[dr]
                else:
                    comps_2d = [0,1]
                
                if dimred_comps_3d and dr in dimred_comps_3d.keys():
                    comps_3d = dimred_comps_3d[dr]
                else:
                    comps_3d = [0,1,2]
                
                if dimred_labels_2d and dr in dimred_labels_2d.keys():
                    labels_2d = dimred_labels_2d[dr]
                else:
                    labels_2d = [f"{name}_{i}" for i in range(2)]
                
                if dimred_labels_3d and dr in dimred_labels_3d.keys():
                    labels_3d = dimred_labels_3d[dr]
                else:
                    labels_3d = [f"{name}_{i}" for i in range(3)]
            self.dimred_infos[dr] = DimredInfo(name=name, labels_2d=labels_2d, labels_3d=labels_3d, comps_2d=comps_2d, comps_3d=comps_3d)
        if default_meta1 is None:
            default_meta1 = sample(list(self.meta_infos.keys()), 1)[0]
        if default_meta2 is None:
            default_meta2 = sample([k for k,v in self.meta_infos.items() if v.meta_type == "cat"], 1)[0]
        if default_meta3 is None:
            default_meta3 = sample([k for k,v in self.meta_infos.items() if v.meta_type == "cat" and k != default_meta2], 1)[0]
        if default_gene1 is None:
            default_gene1 = sample(list(self.adata.var_names), 1)[0]
        if default_gene2 is None:
            default_gene2 = sample(list(self.adata.var_names), 1)[0]
        if default_gene3 is None:
            default_gene3 = sample(list(self.adata.var_names), 1)[0]
        if default_subset_meta is None:
            default_subset_meta = sample([k for k,v in self.meta_infos.items() if v.meta_type == "cat"], 1)[0]
        if default_dimred is None:
            default_dimred = sample(list(self.dimred_infos.keys()), 1)[0]
        if default_genes_list is None:
            default_genes_list = sample(list(self.adata.var_names), 10)
        
        self.ui_defaults = UIDefaults(default_subset_meta=default_subset_meta, 
                                        default_meta1=default_meta1, 
                                        default_meta2=default_meta2, 
                                        default_meta3=default_meta3, 
                                        default_dimred=default_dimred, 
                                        default_gene1=default_gene1, 
                                        default_gene2=default_gene2, 
                                        default_gene3=default_gene3,
                                        default_genes_list=default_genes_list)
    
    def add_meta(self, 
                 meta_id:str,
                 meta_name:str=None,
                 meta_type:str=None,
                 meta_vals:List[str]=None,
                 meta_colors:List[str]=None):
        """Add a meta variable to the dashboard.
        
        :param meta_id: 
            Meta variable id to be added.
        :param meta_name: 
            Name of the meta variable to be used on UI. If None, name will be upper case of the meta id
        :param meta_type: 
            Type of the meta variable. cat or num are the options. If None, type will be inferred from the adata.obs dataframe
        :param meta_vals: 
            List of values for the meta variable. This attribute also determines the order of the values for this meta info. If None, a random ordered list of all values will be used
        :param meta_colors: 
            List of colors for the meta variable for each value in vals. If None, colors will be generated automatically
        """
        if meta_id in self.meta_infos.keys():
            raise ValueError(f"Meta {meta_id} already exists")
        elif meta_id not in self.meta_data.columns:
            raise ValueError(f"Meta {meta_id} not in adata.obs")
        else:
            if meta_name is None:
                meta_name = meta_id.upper()
            if meta_type is None:
                meta_type = "cat" if meta_id in self.meta_data.select(cs.string() | cs.categorical()).columns else "num"
            if meta_type == "cat":
                vals = self.meta_data[meta_id].unique().to_list()
                if meta_vals is None:
                    meta_vals = vals
                else:
                    if len(meta_vals) != len(vals):
                        raise ValueError(f"Meta values for {meta_id} are wrong length")
                if meta_colors is None:
                    meta_colors = [get_hex(c) for c in get_colors(len(vals))]
                else:
                    if len(meta_colors) != len(vals):
                        raise ValueError(f"Meta colors for {meta_id} are wrong length")
        self.meta_infos[meta_id] = MetaInfo(meta_type=meta_type, vals=meta_vals, colors=meta_colors, name=meta_name)
    
    def add_dimred(self, 
                   dimred_id:str,
                   dimred_name:str=None,
                   labels_2d:List[str]=None,
                   labels_3d:List[str]=None,
                   comps_2d:List[str]=None,
                   comps_3d:List[str]=None):
        """Add a dimensionality reduction variable to the dashboard.
        :param dimred_id:
            Dimensionality reduction variable id to be added.
        :param dimred_name:
            Name of the dimensionality reduction variable to be used on UI. If None, name will be upper case of the dimred id
        :param labels_2d:
            Labels for axes for any 2D plot this dimred variable will be used in. If None, labels will be generated name_{i} for i corresponds to dimred component index
        :param labels_3d:
            Labels for axes for any 3D plot this dimred variable will be used in. If None, labels will be generated name_{i} for i corresponds to dimred component index
        :param comps_2d:
            Which components to use for 2D plots using this dimred variable. If None, 0 and 1 will be used
        :param comps_3d:
            Which components to use for 3D plots using this dimred variable. If None, 0, 1 and 2 will be used
        """
        if dimred_id in self.dimred_infos.keys():
            raise ValueError(f"Dimred {dimred_id} already exists")
        elif dimred_id not in self.adata.obsm.keys():
            raise ValueError(f"Dimred {dimred_id} not in adata.obsm")
        else:
            if dimred_name is None:
                dimred_name = dimred_id.upper()
            if labels_2d is None:
                labels_2d = [f"{dimred_name}_{i}" for i in range(2)]
            if labels_3d is None:
                labels_3d = [f"{dimred_name}_{i}" for i in range(3)]
            if comps_2d is None:
                comps_2d = [0,1]
            if comps_3d is None:
                comps_3d = [0,1,2]
        self.dimred_infos[dimred_id] = DimredInfo(name=dimred_name, labels_2d=labels_2d, labels_3d=labels_3d, comps_2d=comps_2d, comps_3d=comps_3d) 
    
    def remove_meta(self, meta:str):
        """
        Remove a meta variable from the dashboard.
        
        :param meta:
            Meta variable id to be removed.
        """
        del self.sclive_dash_config["meta_info"][meta]

    def remove_metas(self, metas:List[str]):
        """
        Remove multiple meta variables from the dashboard.
        
        :param metas: 
            List of meta variable ids to be removed.
        """
        for meta in metas:
            del self.sclive_dash_config["meta_info"][meta]

    def update_meta(self, **kwargs):
        """Update a meta variable in the dashboard.
        
        :param kwargs:
            Dictionary of meta variables with metainfo objects to be updated.
        """
        for key, value in kwargs.items():
            if key in self.sclive_dash_config["meta_info"].keys():
                self.sclive_dash_config["meta_info"][key] = value
            else:
                raise ValueError(f"Meta {key} does not exist")
            
    def order_and_or_subset_meta(self, metas:List[str]):
        """
        Order and/or subset meta variables in the dashboard.
        
        :param metas:
            List of meta variables to indicate new order and/or subset
        """
        self.sclive_dash_config["meta"] = OrderedDict([(meta, self.sclive_dash_config["meta_info"][meta]) for meta in metas])
