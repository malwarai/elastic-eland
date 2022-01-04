from event_data import get_event_data, generate_event_graph_apache_errors


if __name__ == 'main':
	data = get_event_data('apache-logs')
	graph = generate_event_graph_apache_errors(data)