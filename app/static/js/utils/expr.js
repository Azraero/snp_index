function check_gene(info){
  var keys = Object.keys(info);
  for(var i = 0; i < keys.length; i++){
    if(info[keys[i]].length == 0){
      createAlert(keys[i] + ' is empty!');
      return false;
    }
    return true;
  }
}
$(document).ready(function(){
  // multiselect plugin
  select_plugin()
  $("#select_file").change(function(){
    var fileSelect = $(this).find("option:selected").text();
    ajaxSend('/expr/select_file/', {'file': fileSelect}, function(data){
      var msg = data.msg;
      if(msg == 'error'){
        createAlert('not find samples!');
        $("#multi_d").empty();
      }else{
        $("#multi_d").empty();
        samples = data.msg;
        for(var i=0;i<samples.length;i++){
          var tmp = $('<option value="' + samples[i] + '">' + samples[i] + '</option>');
          tmp.appendTo('#multi_d');
        }
      }
    });
  });
  $('#submit').click(function(){
    var gene_name = $("#gene_name").val();
    var table = $("#select_file").find("option:selected").text();
    var groupA = [];
    var groupB = [];
    $("#multi_d_to option").each(function(){
      groupA.push($(this).text());
    });
    $("#multi_d_to_2 option").each(function(){
      groupB.push($(this).text());
    });
    var info = {'gene_name': gene_name,
                'table': table,
                'groupA': groupA,
                'groupB': groupB}
    if(check_gene(info)){
      info = JSON.stringify(info);
      $("#query_hint").empty();
      var hint = $('<span><img src="../static/images/hint.gif" />' + 'loading data, please wait...</span>');
      hint.appendTo('#query_hint');
      ajaxSend('/expr/get_expr_info',{'info': info}, function(data){
        if(data.msg != 'ok'){
          createAlert(data.msg);
          $("#query_hint").empty();
          return;
        }else{
          $("#results-plot").empty();
          $("#query_hint").empty();
          var tmp = $('<div id="main" style="width: 1250px;height:400px;"></div>');
          tmp.appendTo("#results-plot");
          generate_plot(createPlotData(groupA, groupB, data.bodyData));
          tableStr = createTable(data.headData, data.bodyData, tableType='expr');
          $("#results-table").html(tableStr);
          $("#region_table").DataTable({
            dom: 'lBfrtip',
            "scrollX": true,
            buttons: [
              'csv'
            ]
          });
        }
      }, 'POST');
    }else{
      return;
    }
    });
});
