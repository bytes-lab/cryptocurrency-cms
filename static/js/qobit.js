$(document).ready(function(){
    load_coins();
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