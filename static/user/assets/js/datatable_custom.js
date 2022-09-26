
var buttonOpt = []
var dataTableOpt = {
    paging:true,
    pageLength: 10,
    lengthChange:true,
    autoWidth:true,
    searching:true,
    bInfo:true,
    bSort:true,
    responsive: true,
}


function range(start, end) {
    return Array(end - start + 1).fill().map((_, idx) => start + idx)
}
var tbl = $('#basic-datatable').children('thead').children('tr').children().length


try {
    if(typeof exportColumn == 'undefined'){
        var exportColumn = range(0,tbl-2)
    }
} catch (error) {
    var exportColumn = range(0,tbl-2)
}


try {
    if(copy_ || print_ || pdf_ || excel_){
        dataTableOpt['dom'] = "lBfrtp"
        dataTableOpt['buttons'] = buttonOpt
    }
    
    if(copy_){
        buttonOpt.push({
            extend:"copy",
            text:'<i class="mdi mdi-content-copy"></i>',
            className:"btn btn-primary",
            titleAttr:"Copy",
            exportOptions:{
                columns:exportColumn
            }
        })
    }
    
    if(print_){
        buttonOpt.push(
            {
                extend:"print",
                text:'<i class="mdi mdi-printer"></i>',
                className:"btn btn-primary",
                titleAttr:"Print",
                exportOptions:{
                    columns:exportColumn
                },
                customize: function(win){
                    $(win.document.body).css("font-size","10pt")
                    $(win.document.body).find("table").addClass('compact').css("font-size","inherit")
                }
        
            },
        )
    }
    
    if(pdf_){
        buttonOpt.push(
            {
                extend:"pdf",
                text:'<i class="mdi mdi-file-pdf-box"></i>',
                className:"btn btn-primary",
                titleAttr:"PDF",
                exportOptions:{
                    columns:exportColumn
                },
                tableHeader:{
                    alignment:'center'
                },
                customize: function(doc){
                    doc.styles.tableHeader.alignment = 'center'; //header pos
                    doc.styles.tableBodyOdd.alignment = 'center';//body even color gray
                    doc.styles.tableBodyEven.alignment = 'center'; //body even color white
                    doc.styles.tableHeader.fontSize = 7; //header fontsize
                    doc.defaultStyle.fontSize = 6; //body fontsize
                    // 100% width table
                    doc.content[1].table.widths = Array(doc.content[1].table.body[1].length+1).join('*').split('');
            
                }
            },
        )
    }
    if(excel_){
        buttonOpt.push(
            {
                extend:"excel",
                text:'<i class="mdi mdi-file-excel"></i>',
                className:"btn btn-primary",
                titleAttr:"Excel",
                exportOptions:{
                    columns:exportColumn
                }
            },
        )
    }
} catch (error) {
    
}

// var buttonOpt = [
//     {
//         extend:"copy",
//         text:'<i class="mdi mdi-content-copy"></i>',
//         className:"btn btn-primary",
//         titleAttr:"Copy",
//         exportOptions:{
//             columns:exportColumn
//         }
//     },
//     {
//         extend:"print",
//         text:'<i class="mdi mdi-printer"></i>',
//         className:"btn btn-primary",
//         titleAttr:"Print",
//         exportOptions:{
//             columns:exportColumn
//         },
//         customize: function(win){
//             $(win.document.body).css("font-size","10pt")
//             $(win.document.body).find("table").addClass('compact').css("font-size","inherit")
//         }

//     },
//     {
//         extend:"excel",
//         text:'<i class="mdi mdi-file-excel"></i>',
//         className:"btn btn-primary",
//         titleAttr:"Excel",
//         exportOptions:{
//             columns:exportColumn
//         }
//     },
//     {
//         extend:"pdf",
//         text:'<i class="mdi mdi-file-pdf-box"></i>',
//         className:"btn btn-primary",
//         titleAttr:"PDF",
//         exportOptions:{
//             columns:exportColumn
//         },
//         tableHeader:{
//             alignment:'center'
//         },
//         customize: function(doc){
//             doc.styles.tableHeader.alignment = 'center'; //header pos
//             doc.styles.tableBodyOdd.alignment = 'center';//body even color gray
//             doc.styles.tableBodyEven.alignment = 'center'; //body even color white
//             doc.styles.tableHeader.fontSize = 7; //header fontsize
//             doc.defaultStyle.fontSize = 6; //body fontsize
//             // 100% width table
//             doc.content[1].table.widths = Array(doc.content[1].table.body[1].length+1).join('*').split('');

//         }
//     },
// ]



$('#basic-datatable').DataTable(dataTableOpt)

try {
    if(copy_ || print_ || pdf_ || excel_){
        $('#basic-datatable_length').css({"display":"none"})
        $('.dt-buttons.btn-group.flex-wrap').css({"margin-bottom":'-45px'})
    }
}catch (error) {

}