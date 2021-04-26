var DocumentManager = {
    init: function(search_type){
	var me = this;
	me.cacheData('documents');
	me.cacheData('meta_tags');
	me.documents = false;
	me.metadata = false;
	me.lunr_index_docs = false;
	me.lunr_index_meta = false;
	me.search_type = search_type;
	$(document).on("submit", ".query-form", function(event) {
	    event.preventDefault();
	    var query = $(this).find('.query').val();
	    var domain = $(this).find('.query-domain').val(); 
	    me.search(query, domain);
	});
	this.updatePattern();
	var query = $.urlParams()['q'];
	if(query){
	    $(document).find('.query').val(query);
	    this.search(query, search_type == 'all' ? 'all' : 'directory');
	}
    },
    // Caches data in local storage if not cached already, local wrapper for utility
    cacheData: function(name){
	$.cacheFile('/documents/' + name + '.json');
    },
    // Gets the data for an item
    getData: function(name){
	return JSON.parse(localStorage.getItem('/documents/' + name + '.json'))
    },
    // Create the lunr indexes if not yet created
    initLunrIndexDocs: function(){
	var me = this;
	if(!me.documents)
	    me.documents = me.getData('documents');
	if(!me.lunr_index_docs)
	    me.lunr_index_docs = lunr(function () {
		this.ref('id');
		for(var f in me.documents['545_1_1']){
		    if(f != 'id'){
			this.field(f);
		    }
		}
		for(var doc in me.documents){
		    this.add(me.documents[doc]);
		}
	    });
    },
    initLunrIndexMeta: function(){
	var me = this;
	if(!me.metadata)
	    me.metadata = me.getData('meta_tags');
	if(!me.lunr_index_meta)
	    me.lunr_index_meta = lunr(function() {
		this.ref('id');
		this.field('id');
		this.field('children')
		this.field('tags')

		for(var tag in me.metadata){
		    this.add({
			'id': tag,
			'children': me.metadata[tag]
		    });
		}
	    });
    },
    // Handles Searching
    search: function(query, domain){
	var me = this;
	if(!query){
	    $('.searchable').toggleClass('displayed', true);
	    this.updatePattern();
	    return;
	}
	// Redirect to the main search page
	if(domain == 'all' && this.search_type != 'all'){
	    window.location.href = '/documents/index.html?q=' + query;
	}
	var results = [];
	if(this.search_type != 'tags'){
	    this.initLunrIndexDocs();
	    results = $.merge(results, this.lunr_index_docs.search(query));
	}
	if(this.search_type != 'documents'){
	    this.initLunrIndexMeta();
	    results = $.merge(results, this.lunr_index_meta.search(query));
	}
	$('.searchable').toggleClass('displayed', false) ;
	if(this.search_Type == 'all'){
	    results.sort(function(a, b){return a.ref < b.ref});
	    
	}
	results.forEach(function(res){
	    $('#' + md5(res['ref'])).toggleClass('displayed', true);
	    me.renderContent(res['ref'])
	});
	this.updatePattern();
	
    },
    // Updates the alternating colors on list views of items
    updatePattern: function(){
	$('.list-group-item.displayed').each(function(i, e){
	    $(e).css('background-color',  ['#fdfdfe', '#d6d8db'][i % 2]);
	});
    },
    // Renders a tag
    renderTag: function(id){
	var $tag = $('<h4 class="searchable displayed">');
	$tag.attr('id', md5(id));
	var $title = $('<a href="/documents/tags/' + id + '.html">');
	$title.append(
	    $('<span class="badge bg-light text-black shadow text-wrap text-left  mx-1 mb-2 p-2">').text(id.split('_')[id.split('_').length - 1]).append(
		$(' <span class="badge badge-light">').text(this.metadata[id].length)));
	$tag.append($title);
	return $tag;
    },
    // Renders a subdirectory list item
    renderDirectory: function(id){
	var $dir = $('<a class="searchable displayed list-group-item">')
	    .attr('href', 'documents/' + id + '.html')
	    .attr('id', md5(id))
	    .text(this.documents[id].interbrigades_code + ' - ' + this.documents[id].name)
	    .append($('<span class="badge badge-light float-right">')
		    .text(this.documents[id].child_count));
	return $dir;

	
    },
    // Renders the content on the page (Automatically detects tags/directory results)
    renderContent: function(id){
	if(id in this.documents)
	    $('.doc_list').append(this.renderDirectory(id));
	else
	    $('.tag_list').append(this.renderTag(id));
    }
};

