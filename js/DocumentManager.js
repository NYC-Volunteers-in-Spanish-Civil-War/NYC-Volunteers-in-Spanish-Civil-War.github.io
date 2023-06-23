var DocumentManager = {
    init: function(search_type){
	var me = this;
	me.documents = false;
	me.metadata = false;
	me.lunr_index_docs = false;
	this.initLunrIndexDocs();
	this.initLunrIndexMeta();
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
    // Create the lunr indexes if not yet created
    initLunrIndexDocs: function(){
	var me = this;
	$.getJSON('/documents/documents.json',function(data){
	    me.documents = data;
	    // generate lunr index for faster searching
	    if(!me.lunr_index_docs){
		me.lunr_index_docs = lunr(function () {
		    this.ref('id');
		    // Get the various fields in the data
		    for(var f in me.documents['545_1_1']){
			if(f != 'id'){
			    this.field(f);
			}
		    }
		    // Add all the rows in the data to the new index
		    for(var doc in me.documents){
			this.add(me.documents[doc]);
		    }
		});
	    };
	});
    },
    initLunrIndexMeta: function(){
	var me = this;
	$.getJSON('/documents/meta_tags.json',function(data){
	    me.metadata = data;
	    // generate lunr index for faster searching
	    if(!me.lunr_index_meta){
		me.lunr_index_meta = lunr(function() {
		    // Get the various fields in the data
		    this.ref('id');
		    this.field('id');
		    this.field('children')
		    this.field('tags')
		    // Add all the rows in the data to the new index
		    for(var tag in me.metadata){
			this.add({
			    'id': tag,
			    'children': me.metadata[tag]
			});
		    }
		});
	    };
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
	// Build the search indices if necessary, then search for matches
	var results = [];
	if(this.search_type != 'tags'){
	    results = $.merge(
		results,
		this.lunr_index_docs.search(query).sort(function(a, b){return me.codeToList(a.ref) > me.codeToList(b.ref)}));
	}
	if(this.search_type != 'documents'){
	    results = $.merge(
		results,
		this.lunr_index_meta.search(query).sort(function(a, b){return a.ref < b.ref}));
	}
	// Remove previously rendered items and generate new ones
	if(this.search_type == 'all')
	    $('.searchable.displayed').remove();
	$('.searchable').toggleClass('displayed', false);
	results.forEach(function(res){
	    $('#' + md5(res['ref'])).toggleClass('displayed', true);
	    domain == 'all' && me.renderContent(res['ref']);
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
	var me = this;
	var $tag = $('<h4 class="searchable displayed">');
	$tag.attr('id', md5(id));
	var url = this.metadata['tags'].includes(id) ?
	    id + '/' :
	    this.metadata['tags'].filter(function(v){
		return me.metadata[v].includes(id);
	    })[0] + '/' + id + '.html';
	var $title = $('<a href="/documents/tags/' + url + '">');
	$title.append(
	    $('<span class="badge bg-light text-black shadow text-wrap text-left  mx-1 mb-2 p-2">').text(id).append(
		$(' <span class="badge badge-light">').text(this.metadata[id].length)));
	$tag.append($title);
	return $tag;
    },
    // Renders a subdirectory list item
    renderDirectory: function(id){
	var $dir = $('<a class="searchable displayed list-group-item">')
	    .attr('href', '/documents/' + id + '.html')
	    .attr('id', md5(id))
	    .html(this.documents[id].interbrigades_code + ' - ' + this.documents[id].name)
	    .append($('<span class="badge badge-light float-right">')
		    .text(this.documents[id].child_count));
	return $dir;

	
    },
    // Renders the content on the page (Automatically detects tags/directory results)
    renderContent: function(id){
	if(this.documents && id in this.documents)
	    $('.doc_list').append(this.renderDirectory(id));
	else
	    $('.tag_list').append(this.renderTag(id));
    },
    // Transforms a directory code into a list of integers
    codeToList: function(code){
	return code.split('_').map( Number );
    }
};

