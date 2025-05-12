mf_common = ['prop','name','domain']

meta_props = {
    'data.Meta': {
        'default': ('pick', ['entity','name']),
    },
    'data.MetaView': {
        'list': ('pick', ['meta_id','code','view_name']),
    },
    'data.MetaField': {
        'add': ('pick',[*mf_common]),
        'tool': ('pick',[*mf_common,'tool','refer','format']),
        'rest': ('pick',[*mf_common,'not_null','allow_edit','allow_sort','allow_search','allow_download','allow_upload','allow_update']),
        'table': ('pick',[*mf_common,'unit','column_width','fixed','align','edit_on_table','hide_on_table','header_color','cell_color']),
        'form': ('pick',[*mf_common,'hide_on_form','hide_on_form_insert','hide_on_form_edit','hide_on_form_branch','hide_on_form_leaf','span']),
    }
}


meta_defaults = {
    'data.MetaField':{
        "prop":{
            'allow_edit': False,
            'column_width': 100
        },
        "domain":{
            'allow_edit': False,
            'column_width': 100
        },
        "tool":{
            'column_width': 100
        },
        "span":{
            'column_width': 100,
            "format": { "min": 0, "max": 24, "step": 1, "precision": 0, "step_strictly": True }
        },
        "refer":{
            'allow_edit': False,
            'column_width': 80
        },
        "format":{
            'allow_edit': False,
            'column_width': 80
        },
    }
}