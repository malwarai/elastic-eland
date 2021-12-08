import eland as ed
from creds import config
import networkx as nx

#Get event data from elastic
def get_event_data( index, eql_query=None, size=1000):
	Es = config.es
	if eql_query:
		events = Es.eql.search(index=index, body = {'query': eql_query, 'size':size})
		return events
	else:
		df = ed.DataFrame(Es, index)
		df = df.to_pandas()
		return df


#Create graph from event data based on ip of the source
def generate_event_graph(df):
	G = nx.Graph()
	hosts = df['host.name']
	k=1
	for d in df.iterrows():
		G.add_node(k, type='source', ip= d[1]['source.ip'])
		k+=1
	return G







