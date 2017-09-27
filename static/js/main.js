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
