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
        if(j == 0){
            href_str = "<a target='_blank' href='/locus_identifier_search?gene=" + bodyData[i][j] + "'>" +
                bodyData[i][j] + "</a>";
            htmlBuffer.push("<td>" + href_str + "</td>");
        }else{
            htmlBuffer.push("<td>" + bodyData[i][j] + "</td>");
        }
    }
    htmlBuffer.push("</tr>");
  }
  htmlBuffer.push("</tbody>");
  htmlBuffer.push("</table>");
  tableStr = htmlBuffer.join('\n');
  return tableStr;
}

function select_plugin(){
  // multiselect plugin
  $('#multi_d').multiselect({
    right: '#multi_d_to, #multi_d_to_2',
    rightSelected: '#multi_d_rightSelected, #multi_d_rightSelected_2',
    leftSelected: '#multi_d_leftSelected, #multi_d_leftSelected_2',
    rightAll: '#multi_d_rightAll, #multi_d_rightAll_2',
    leftAll: '#multi_d_leftAll, #multi_d_leftAll_2',

    search: {
        left: '<input type="text" name="q" class="form-control" placeholder="Search..." />'
    },

    moveToRight: function(Multiselect, $options, event, silent, skipStack) {
        var button = $(event.currentTarget).attr('id');

        if (button == 'multi_d_rightSelected') {
            var $left_options = Multiselect.$left.find('> option:selected');
            Multiselect.$right.eq(0).append($left_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$right.eq(0).find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$right.eq(0));
            }
        } else if (button == 'multi_d_rightAll') {
            var $left_options = Multiselect.$left.children(':visible');
            Multiselect.$right.eq(0).append($left_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$right.eq(0).find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$right.eq(0));
            }
        } else if (button == 'multi_d_rightSelected_2') {
            var $left_options = Multiselect.$left.find('> option:selected');
            Multiselect.$right.eq(1).append($left_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$right.eq(1).find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$right.eq(1));
            }
        } else if (button == 'multi_d_rightAll_2') {
            var $left_options = Multiselect.$left.children(':visible');
            Multiselect.$right.eq(1).append($left_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$right.eq(1).eq(1).find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$right.eq(1));
            }
        }
    },

    moveToLeft: function(Multiselect, $options, event, silent, skipStack) {
        var button = $(event.currentTarget).attr('id');

        if (button == 'multi_d_leftSelected') {
            var $right_options = Multiselect.$right.eq(0).find('> option:selected');
            Multiselect.$left.append($right_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$left.find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$left);
            }
        } else if (button == 'multi_d_leftAll') {
            var $right_options = Multiselect.$right.eq(0).children(':visible');
            Multiselect.$left.append($right_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$left.find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$left);
            }
        } else if (button == 'multi_d_leftSelected_2') {
            var $right_options = Multiselect.$right.eq(1).find('> option:selected');
            Multiselect.$left.append($right_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$left.find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$left);
            }
        } else if (button == 'multi_d_leftAll_2') {
            var $right_options = Multiselect.$right.eq(1).children(':visible');
            Multiselect.$left.append($right_options);

            if ( typeof Multiselect.callbacks.sort == 'function' && !silent ) {
                Multiselect.$left.find('> option').sort(Multiselect.callbacks.sort).appendTo(Multiselect.$left);
            }
        }
    }
  });
}

function generate_plot(info){
  var myChart = echarts.init(document.getElementById('main'));
  var option = {
         title: {},
         tooltip: {
           /*
           trigger: 'axis',
           axisPointer: {
             type: 'shadow',
             label: {
               show: true
             }
           }
           */
         },
         toolbox: {
           show: true,
           orient: 'vertical',
           x: 'right',
           y: 'center',
           feature: {
             mark: {show: true},
             magicType: {show: true, type: ['line', 'bar']},
             restore: {show: true},
             saveAsImage: {show: true}
           }
         },
         legend: {
             data: info['gene_name']
         },
         xAxis: {
             data: info['xlabel']
         },
         yAxis: {
           type: 'value',
           name: 'expression quantity(log2)'
         },
         series: info['series']
     };
     // 使用刚指定的配置项和数据显示图表。
     myChart.setOption(option);
}
function add_line(lineA, lineB){
  if(lineA.length !== lineB.length){
    alert('array length must be eq!');
    return;
  }else{
    for(var i=0;i<lineA.length;i++){
      lineA[i] = lineA[i] + lineB[i];
    }
    return lineA;
  }
}
function createPlotData(groupA, groupB, data){
  var xlabel = groupA.concat(groupB);
  var gene_ids = [];
  var series = [];
  var line = [];
  var avg_line = [];
  for(var i=0;i<data.length;i++){
    var tmpObj = {};
    line = data[i].slice(4,data[i].length).map(function(item, index, arr){
      // log2
      return Math.log(Number(item) + 1) / Math.log(2);
    });
    gene_ids.push(data[i][0]);
    tmpObj['name'] = data[i][0];
    tmpObj['type'] = 'line',
    tmpObj['data'] = line;
    series.push(tmpObj);
  }
  var plotInfo = {
    'gene_name': gene_ids,
    'xlabel': xlabel,
    'series': series
  }
  //console.log(plotInfo);
  return plotInfo;
}
