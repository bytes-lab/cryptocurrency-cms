$(document).ready(function(){
    load_coins();
    load_all_coins();
    load_master_coins();
	load_exchanges();
	load_exchange_detail();
	load_supported_exchanges();
});

function load_coins() {
    $("#data-table-coins").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"#" + row.id + "\"><span class=\"zmdi zmdi-plus\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });
}

function load_master_coins() {
    $("#data-table-master-coins").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"#" + row.id + "\"><span class=\"zmdi zmdi-plus\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });
}

function load_all_coins() {
    $("#data-table-all-coins").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"#" + row.id + "\"><span class=\"zmdi zmdi-plus\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
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
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });    
}

function load_exchange_detail() {
    var grid = $("#data-table-exchange-detail").bootgrid({
        css: {
            icon: 'zmdi icon',
            iconColumns: 'zmdi-view-module',
            iconDown: 'zmdi-expand-more',
            iconRefresh: 'zmdi-refresh',
            iconUp: 'zmdi-expand-less'
        },
        formatters: {
            "newline": function (column, row) {
                return row[column.id].replace(/@/g, '<br>');
            },
            "commands": function(column, row) {
                if (row.supported == 'YES') {
                    return '<div class="text-success m-5 f-500 f-15">N/A</div>';
                } else {
                    return "<a type=\"button\" class=\"btn btn-icon command-add waves-effect waves-circle\" data-row-id=\"" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
                }

            }
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Coins',
            noResults: 'There is no record'
        },
        templates: {
            footer: "",
            header: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
        rowCount: [15],
        requestHandler: function (request) {
            var model = {
                current: request.current,
                rowCount: request.rowCount,
            };

            return JSON.stringify(model);
        }                
    }).on("loaded.rs.jquery.bootgrid", function() {
        grid.find(".command-add").on("click", function(e) {
            var item_id = $(this).data("row-id");
            //Warning Message
            if ($('.supported-exchange').length == 0) {
                swal({title:"Notification!", text:"The exchange is not supported.", type:"warning"}, 
                                    function() {});                
            } else {
                location.href = "/add_pair/" + item_id;
            }
        });
    });        
}

function load_supported_exchanges() {
    $("#data-table-supported-exchanges").bootgrid({
        formatters: {
            "commands": function(column, row) {
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/exchanges/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
            }
        },
        templates: {
            header: '<div id="{{ctx.id}}" class="{{css.header}}"><div class="row m-t-15"><div class="col-sm-6 p-0"><p class="{{css.search}}"></p></div>',
            footer: '<div id="{{ctx.id}}" class="{{css.footer}}"><div class="row m-t-15"><div class="col-sm-6"><p class="{{css.pagination}}"></p></div><div class="col-sm-6 infoBar"><p class="{{css.infos}}"></p></div></div></div>'
        },
        ajaxSettings: {
            method: "POST",
            cache: false
        },
    });    
}
