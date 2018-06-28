$(document).ready(function(){
    load_master_coins();
	load_exchanges();
	load_exchange_detail();
	load_supported_exchanges();
});

function load_master_coins() {
    $("#data-table-master-coins").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/attach_coin/" + row.id + "\"><span class=\"zmdi zmdi-edit\"></span></a>"+
                    "<a type=\"button\" target=\"_blank\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/admin/general/mastercoin/" + row.id + "/change\"><span class=\"zmdi zmdi-assignment\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        rowCount: [30],
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });
}

function load_exchanges() {
    $("#data-table-exchanges").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/exchanges/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        rowCount: [30],
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });    
}

function load_exchange_detail() {    
    var grid = $("#data-table-exchange-detail").bootgrid({
        formatters: {
            "commands": function(column, row) {
                if (row.supported == 'YES') {
                    return '<div class="text-success m-5 f-500 f-15">N/A</div>';
                } else if ($('.supported-exchange').length == 0) {
                    return '<div class="text-danger m-5 f-500 f-15">N/A</div>';
                } else {
                    var exchange = row.exchange;
                    if (!row.coin_supported || !row.quote_coin_supported) {
                        exchange = -1;
                    }
                    return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" data-row-pair=\"" + row.pair + "\" data-exchange=\""+exchange+"\"><span class=\"zmdi zmdi-plus\"></span></a>";
                }
            },
            "coins": function(column, row) {
                if (row.coin_supported) {
                    return row.coin;
                } else if (row.coin) {
                    return "<span class='p-r-10'>"+row.coin+"</span>"+ "<a class='btn bgm-blue btn-xs waves-effect' href='/add_coin/"+row.coin+"/"+row.exchange+"' title='Add a base coin'>Link</a>";
                }
            },
            "pair": function(column, row) {
                if (row.quote_coin_supported) {
                    return row.pair;
                } else {
                    return "<span class='p-r-10'>"+row.pair+"</span>"+ "<a class='btn bgm-blue btn-xs waves-effect' href='/add_coin/"+row.quote_coin+"/"+row.exchange+"' title='Add a quote coin'>Link</a>";
                }
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        rowCount: [30],
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    }).on("loaded.rs.jquery.bootgrid", function() {
        grid.find(".command-edit").on("click", function(e) {
            var pair = $(this).data("row-pair").replace(' / ', '-');
            var exchange = $(this).data("exchange");
            //Warning Message
            if (exchange < 0) {
                swal({title:"Notification!", text:"The base coin or quote coin is not supported. Please add them first.", type:"warning"}, 
                                    function() {});                
            } else {
                var url = "/add_pair/" + exchange + '/' + pair;
                window.open(url,'_blank');
            }
        });
    });        
}

function load_supported_exchanges() {
    $("#data-table-supported-exchanges").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/exchanges/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
            },
            "new_pairs": function(column, row) {
                if (row.num_new_pairs > 0) {
                    return "<a class='btn bgm-red btn-xs waves-effect' href='#' title='Add a base coin'>"+row.num_new_pairs+"</a>";
                } else {
                    return '<div class="text-success m-5 f-500 f-15">N/A</div>';
                }
            },
            "new_coins": function(column, row) {
                if (row.num_new_coins > 0) {
                    return "<a class='btn bgm-red btn-xs waves-effect' href='#' title='Add a coin'>"+row.num_new_coins+"</a>";
                } else {
                    return '<div class="text-success m-5 f-500 f-15">N/A</div>';
                }
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        rowCount: [30],
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });    
}
