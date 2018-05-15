$(document).ready(function(){
    load_coins();
	load_exchanges();
	load_exchange_detail();
	load_supported_exchanges();
});

function load_coins() {
    $("#data-table-coins").bootgrid({
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
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/print_history/" + row.id + "\"><span class=\"zmdi zmdi-edit\"></span></a>";
            }
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Coins',
            noResults: 'There is no coin'
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
    });        
}

function load_exchanges() {
    $("#data-table-exchanges").bootgrid({
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
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/exchanges/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
            }
        },
        labels: {
            infos: 'Showing {{ctx.start}} to {{ctx.end}} of {{ctx.total}} Coins',
            noResults: 'There is no coin'
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
    });        
}

function load_exchange_detail() {
    $("#data-table-exchange-detail").bootgrid({
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
                    return '<span class="text-success m-l-5 f-500 f-15">N/A</span>';
                } else {
                    return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/add_pair/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
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
    });        
}

function load_supported_exchanges() {
    $("#data-table-supported-exchanges").bootgrid({
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
                return "<a type=\"button\" class=\"btn btn-icon command-edit waves-effect waves-circle\" href=\"/exchanges/" + row.id + "\"><span class=\"zmdi zmdi-eye\"></span></a>";
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
    });        
}