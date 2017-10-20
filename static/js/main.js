function ajaxSend(reqUest_url, post_data, callback, request_method, return_type, dict_vars) {
    var params = {
    url: reqUest_url,
    data: post_data || '',
    type: request_method || 'GET',
    success: callback,
    error: function (request, textStatus, errorThrown) {
        alert("Request failed, please try again.");
    },
    return_type: return_type || 'json',
    cache: false,
    global: true,
    ajax_func_flag: false,
    custom_func: callback
    };
    if (dict_vars) {
        for (var key in dict_vars) {
            params[key] = dict_vars[key];
        }
    }
    $.ajax(params);
}

function get_input_data(){
  var table = $("#select_file").find("option:selected").text();
  var chr = $("#select-chr").find("option:selected").text();
  var startPos = $("#pos-start").val();
  var endPos = $("#pos-end").val();
  var groupA = [];
  var groupB = [];
  $("#multi_d_to option").each(function(){
    groupA.push($(this).text());
  });
  $("#multi_d_to_2 option").each(function(){
    groupB.push($(this).text());
  });
  var all_info = {
    'table': table,
    'chr': chr,
    'start_pos': startPos,
    'end_pos': endPos,
    'groupA': groupA,
    'groupB': groupB,
  };
  return all_info;
}

function check_input_data(info){
  var pos_max = 1000000;
  var error_msg = '';
  if(! info['chr']){
    return '请选择染色体!';
  }else if(! info['start_pos']){
    return '请输入起始位置!';
  }else if(! info['end_pos']){
    return '请输入结束位置!';
  }else if(info['end_pos'] - info['start_pos'] > pos_max){
    return '查看长度应该小于1mb!';
  }else if(info['groupA'].length == 0){
    return '请选取 groupA 比对的样品!';
  }else if(info['groupB'].length == 0){
    return '请选取 groupB 比对的样品!';
  }else{
    return error_msg;
  }
}

function createTable(headData, bodyData) {
  var htmlBuffer = [];
  htmlBuffer.push("<table id='region_table' class='table table-strip table-bordered'>");
  // for header
  htmlBuffer.push("<thead>\n<tr>");
  for(var i = 0; i < headData.length; i++){
      htmlBuffer.push("<th>" + headData[i] + "</th>");
  }
  htmlBuffer.push("</tr>\n</thead>");
  // for body
  htmlBuffer.push("<tbody>");
  for(var i = 0; i < bodyData.length; i++){
    htmlBuffer.push("<tr>");
    for(var j = 0; j < bodyData[i].length; j++){
      htmlBuffer.push("<td>" + bodyData[i][j] + "</td>");
    }
    htmlBuffer.push("</tr>");
  }
  htmlBuffer.push("</tbody>");
  htmlBuffer.push("</table>");
  tableStr = htmlBuffer.join('\n');
  return tableStr;
}
