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
    // Caches the data and a expiry time 4 hours in the future
    $.cacheData = function(name, data){
	localStorage.setItem(name, JSON.stringify(data));
	localStorage.setItem(name + "_expiry", (new Date()).getTime() + (60 * 60 * 4));
    }
    // Caches a file in local storage, 4 hour expiry
    $.cacheFile = function(name){
	if(!localStorage.getItem(name)){
	    $.getJSON(name, function(data){
		$.cacheData(name, data);
	    });
	}
    }
    // Gets the data
    $.getData = function(name){
	return JSON.parse(localStorage.getItem(name));
    }

}());
