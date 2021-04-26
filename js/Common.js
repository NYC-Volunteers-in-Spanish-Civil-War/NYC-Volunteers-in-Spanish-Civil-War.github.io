$(function(){
     // Returns an object containing key-value pairs contained in the pages GET data
     $.urlParams = function(){
	 var items = {};
	 window.location.search.substring(1).split('&').map(function(i){
    	     var k = i.split('=');
    	     items[k[0]] = decodeURIComponent(k[1]);
	 });
	 return items;
     }
     // Caches a file in local storage if not cached already;
     $.cacheFile = function(name){
	 if(!localStorage.getItem(name)){
	     $.getJSON(name, function(data){
		 localStorage.setItem(name, JSON.stringify(data));
	     });
	 }
     }
}());
