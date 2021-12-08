// chrome.runtime.onMessage.addListener(function(message, callback) {
//     alert("in bg")
//     if (message.data == "setAlarm") {
//       chrome.alarms.create({delayInMinutes: 5})
//     } else if (message.data == "changeColor") {
//       chrome.tabs.executeScript(
//           {code: 'document.body.style.backgroundColor="orange"'});
//     } else {
//         alert(message.data+"in bg")
//     };
//   });
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
    //    alert("background received "+request.data.labelName)
    //   console.log(sender.tab ?
    //               "from a content script:" + sender.tab.url :
    //               "from the extension");
    let json = JSON.stringify(request.data);
    fetch("http://127.0.0.1:5000/", {
      method: "POST",
      body:json
    }).then(r=>r.text())
    .then(response => {
      alert("fetched", response);
    })
      //if (request == "ak")
        sendResponse("goodbye");
    }
  );