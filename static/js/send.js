function Send(url, dic, callback) {
  if (url[url.length - 1] == '/') {
    url = url.slice(0, url.length - 1)
  }

  loader = document.getElementById('loader')
  if (loader) {
    loader.style.display = 'block'
  }
  $(function () {
    $.ajax({
      url: url + Dic2ParamString(dic),
      type: 'GET',
      contentType: 'application/json',
    })
      .done((res) => {
        console.log(res)
        loader = document.getElementById('loader')
        if (loader) {
          loader.style.display = 'none'
        }
        if (callback) {
          callback(res)
        }
      })
      .fail((res) => {
        if(loader){
          loader.style.display = 'none'
        }
        window.alert('通信に失敗しました')
        console.log(res);
      })
  });
}

function Dic2ParamString(obj) {
  let str = "?";
  for (var key in obj) {
    if (str != "") {
      str += "&";
    }
    str += key + "=" + encodeURIComponent(obj[key]);
  }
  return str
}
