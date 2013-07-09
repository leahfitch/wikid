;(function ()
{
	var $search = $('#wikid-search'),
		$input = $search.find('input'),
		$results = $search.find('.results'),
		$cancel = $search.find('.cancel'),
		base_path = (function ()
		{
			var rel_parts = $('script:first').attr('src').split('/').slice(0,-2),
				path_parts = window.location.pathname.split('/').slice(0,-1)
			
			$.each(rel_parts, function ()
			{
				if (this == '.')
				{
					return
				}
				
				if (this == '..')
				{
					path_parts.pop()
				}
				else
				{
					path_parts.push(this)
				}
			})
			
			var path = path_parts.join('/')
			
			if (path[path.length - 1] != '/')
			{
				path += '/'
			}
			
			return path
		})()
	
	;(function ()
	{
		var get_values = function (node)
		{
			var values = []

			if (node.v)
			{
				values = values.concat(node.v)
			}

			if (node.c)
			{
				for (k in node.c)
				{
					values = values.concat(get_values(node.c[k]))
				}
			}

			return values
		}

		var get_prefix_matches = function (node, prefix)
		{
			if (!prefix)
			{
				return node.v || []
			}

			if (!node.c)
			{
				return []
			}

			var values = []

			for (var n in node.c)
			{
				if (prefix.length <= n.length)
				{
					if (n.indexOf(prefix) === 0)
					{
						values = values.concat(get_values(node.c[n]))
					}
				}
				else if (node.c[n].c && prefix.indexOf(n) === 0)
				{
					values = values.concat( get_prefix_matches(node.c[n], prefix.substr(n.length)) )
				}
			}

			return values
		}

		var get_full_records_from_matches = function (matches)
		{
			var records = []

			$.each(matches, function (i, match)
			{
				var record = {
					relevance: match[0],
					path: wikid_search_index.paths[match[1]],
					title: wikid_search_index.titles[match[2]],
					context: match[3] || ''
				}
				
				if (record.context)
				{
					if (record.context[0] == '.')
					{
						record.context = '..' + record.context
					}

					if (record.context[record.context.length-1] == '.')
					{
						record.context = record.context + '..'
					}					
				}

				records.push(record)
			})

			return records
		}

		var sort_matches = function (matches)
		{
			matches.sort(function (a, b)
			{
				return b.relevance - a.relevance
			})
		}

		var get_filtered_matches = function (matches)
		{
			var paths_seen = {},
				new_matches = []

			for (var i=0; i<matches.length; i++)
			{
				if (paths_seen[matches[i].path])
				{
					continue
				}

				paths_seen[matches[i].path] = 1
				new_matches.push(matches[i])
			}

			return new_matches
		}

		var hilite_context = function (search_text, matches)
		{
			var escaped_search_text = search_text.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&"),
				pattern = new RegExp('('+escaped_search_text+')', 'gi')

			for (var i=0; i<matches.length; i++)
			{
				// If the match is with a term in the title then the context
				// is the title
				var n = matches[i].context ? 'context' : 'title',
					c = matches[i][n]

				matches[i][n] = c.replace(pattern, '<span class="match">$1</span>')
			}
		}

		var adjust_paths = function (matches)
		{
			for (var i=0; i<matches.length; i++)
			{
				matches[i].path = base_path + matches[i].path
			}
		}

		var find = function (text)
		{
			var text = text.replace(/\s+\:\;\(\)\{\}\[\]\,\?\!\./gi, '').toLowerCase(),
				matches = get_full_records_from_matches(
							get_prefix_matches(wikid_search_index.trie, text))

			sort_matches(matches)
			matches = get_filtered_matches(matches)
			hilite_context(text, matches)
			adjust_paths(matches)

			return matches
		}

		var last_search_text = '',
			$results_list = null

		var select_next_result = function ()
		{
			var $items = $results_list.find('>li')
				$selected = $items.filter('.selected'),
				i = $selected.index(),
				$next = $items.eq( (i+1) % $items.length )
				
			$selected.removeClass('selected')
			$next.addClass('selected')
		}

		var select_previous_result = function ()
		{
			var $items = $results_list.find('>li')
				$selected = $items.filter('.selected'),
				i = $selected.index() - 1,
				$prev = $items.eq( i < 0 ? $items.length-1 : i )
				
			$selected.removeClass('selected')
			$prev.addClass('selected')
		}

		var go_to_selected_result = function ()
		{
			var $link = $results_list.find('>li.selected a')
			window.location.href = $link.attr('href')
		}

		var hide_search_results = function ()
		{
			last_search_text = ''
			$input.val('')
			$results.hide()
			$(document).unbind('click', hide_search_results)
			$cancel.hide()
		}

		var update_search_results = function ()
		{
			var search_text = $input.val()

			if (search_text == last_search_text)
			{
				return
			}

			last_search_text = search_text

			var matches = find(search_text)

			if (matches.length > 0)
			{
				$results_list = $('<ul></ul>')

				$.each(matches, function (i, match)
				{
					var $li = $('<li></li>'),
						$a = $('<a href="'+match.path+'"></a>')

					if (match.title)
					{
						$a.append($('<span class="title">'+(match.title ? match.title : match.title)+'</span>'))
					}

					if (match.context)
					{
						$a.append($('<span class="'+(match.title ? 'context' : 'title')+'">'+match.context+'</span>'))
					}

					$li.append($a)
					$results_list.append($li)
				})

				$results.html('').append($results_list)

				$results_list.find('li:first').addClass('selected')

				if ($results.is(':hidden'))
				{
					$cancel.show()
					$results.show()
					$(document).bind('click', hide_search_results)
				}
			}
			else
			{
				hide_search_results()
			}
		}

		$cancel.click(function (e)
		{
			e.preventDefault()
			hide_search_results()
		})
		
		$results.click(function (e)
		{
			hide_search_results()
		})
		
		$input
			.keyup(function (e)
			{
				switch(e.keyCode)
				{
					case 40:
						select_next_result()
						break
					case 38:
						select_previous_result()
						break
					case 13:
						go_to_selected_result()
						break
					case 9:
					case 27:
						hide_search_results()
						break
					default:
						update_search_results()
				}
			})
			.focus(update_search_results)

		$search.click(function (e)
		{
			e.stopPropagation()
		})
	})()
	
	var clean_path = function (path)
	{
		path = path.toLowerCase()
		if (path[path.length - 1] == '/')
		{
			path = path.substr(0, path.length - 1)
		}
		
		return path
	}
	
	var is_on_current_page = function (path)
	{
		var parts = path.split('#')
		return clean_path(parts[0]) == clean_path(window.location.pathname)
	}
	
	var complete_path = function (path)
	{
		if (path[0] == '/')
		{
			return base_path + path.substr(1)
		}
		else
		{
			return base_path + path
		}
	}
	
	;(function ()
	{
		var $toc = $('#wikid-toc')
			$curlist = $('<ul></ul>'),
			$curitem = null,
			depth = 1
		
		$toc.append($curlist)
		
		$.each(wikid_toc, function ()
		{
			if (this.depth > depth)
			{
				for (var i=0; i<this.depth-depth; i++)
				{
					$curlist = $('<ul></ul>')
					$curitem.append($curlist)
				}
			}
			else if (this.depth < depth)
			{
				for (var i=0; i<depth-this.depth; i++)
				{
					$curlist = $curlist.parent().parent()
				}
			}
			
			var path = complete_path(this.path)
			$curitem = $('<li></li>')
			$curitem.append(
				$('<a>'+this.text+'</a>').attr('href', path)
			)
			$curlist.append($curitem)
			
			depth = this.depth
			
			if (is_on_current_page(path))
			{
				$curitem.addClass('current')
			}
		})
		
		$toc.find('>ul>li').each(function ()
		{
			var $item = $(this),
				$disclosure = $('<a href="#" class="disclosure"></a>')
			$item.prepend($disclosure)
			
			if ($item.find('ul').length == 0)
			{
				$disclosure
					.addClass('hidden')
					.click(function (e)
					{
						e.preventDefault()
					})
				return
			}
			
			if ($item.is('.current'))
			{
				$item.addClass('open')
				$disclosure.html('-')
			}
			else
			{
				$disclosure.html('+')
			}
			
			$disclosure.click(function (e)
			{
				e.preventDefault()
				
				if ($item.is('.open'))
				{
					$item.removeClass('open')
					$disclosure.html('+')
				}
				else
				{
					$item.addClass('open')
					$disclosure.html('-')
				}
			})
		})
	})()
})()