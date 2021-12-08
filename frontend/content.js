//alert('The word "lottery" is found in this email, it might be a spam')
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    
    const re = new RegExp('lottery', 'gi')
    //alert(re)
    // if(re==undefined){
    //     alert('Nothing was found, this page is safe')
    // } 
    // else {
    //     alert('This page contains suspicious words')
    // }
    const matches = document.documentElement.innerHTML.match(re)
    //alert( matches)
    if(matches==null){
        alert('Nothing suspicious found, this page is likely safe')
    } 
    sendResponse({count: matches.length})

})