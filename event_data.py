import eland as ed
from creds import config
import networkx as nx


#Get event data from elastic
def get_event_data(index, eql_query=None, size=1000):
	Es = config.es
	if eql_query:
		events = Es.eql.search(index=index, body = {'query': eql_query, 'size':size})
		return events
	else:
		df = ed.DataFrame(Es, index)
		df = df.to_pandas()
		return df


#Create graph from event data based on ip of the source
def generate_event_graph_apache_errors(df):
	G = nx.Graph()
	hosts = list(df['host.name'].unique())
	k=1
	for h in hosts:
		G.add_node(k, type='host', hostname = h, color='blue')
		k+=1
	for d in df.iterrows():
		G.add_node(k, type='source', ip= d[1]['source.ip'], color='yellow', country=d[1]['source.geo.country_name'], \
		           response = d[1]['http.response.status_code'], referrer=d[1]['http.request.referrer'])
		G.add_edges_from([(k, hosts.index(d[1]['host.name'])+1)])
		newData = df[(df['source.ip'] == d[1]['source.ip']) & (df['host.name'] ==d[1]['host.name'])]
		severity = attack_severity(newData)
		nx.set_edge_attributes(G, {(k, hosts.index(d[1]['host.name'])+1): {"severity": severity}})
		k+=1
	return G


#define attack severity based on the url pattern of the host and the number of cases
def attack_severity(data):
	unique_url_paths =list(data['url.path'].unique())
	score = [find_vulnerability_score(u) for u in unique_url_paths]
	return sum(score)


def find_vulnerability_score(indicator):
	# TODO: use an API to determine how the indicator is related to an existing vuln., e.g. CVE database
	# severity should be related to the CVSS or other vuln scoring system.
	severity=1
	return severity