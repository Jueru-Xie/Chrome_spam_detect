document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('button').addEventListener('click', onclick, false)
  
  function onclick () {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs) {
      chrome.tabs.sendMessage(tabs[0].id, 'hi', setCount)
      
    })
    //alert("haha")
    submit()
  }
  
  function submit(){
    let labelName = document.getElementById("labelName").value;
    if(labelName==""){
      alert("trying to send label msg")
      let newLabelName = document.getElementById("newLabelName").value;
      let keyword = document.getElementById("keyword").value;
      let start = document.getElementById("start").value;
      let end = document.getElementById("end").value;
      
      let data = {
        service:"label",
        newLabelName:newLabelName, 
        keyword:keyword,
        start:start,
        end:end
        };
      
      chrome.runtime.sendMessage({
        data
    }, function(response) {
        alert(response);
      });
    } else {
      alert("trying to send reply msg")
      let labelName = document.getElementById("labelName").value;
      let template = document.getElementById("template").value;
      let title = document.getElementById("title").value;
      let replyBody = document.getElementById("replyBody").value;
      let tempType = document.getElementById("tempType").value;
      
      let data = {
        service:"send",
        labelName:labelName, 
        template:template,
        title:title,
        replyBody:replyBody,
        tempType:tempType};
      alert("in submit function")
      // chrome.runtime.sendMessage({
      //   type: "postData",
      //   data
      // }, response => {
      //   response = JSON.parse(response);
      // });
      chrome.runtime.sendMessage({
        data
    }, function(response) {
        alert(response);
      });
    }

    
  }

  function setCount(res) {
    const div = document.createElement('div')
    div.textContent = `The word 'lottery' was found la times, this page likely contains a spam.`
    //  
    // if(1==1){
    //     div.textContent = div.textContent+('\nasa')
    // }
    document.body.appendChild(div)
    }

}, false)