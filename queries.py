import json

def all_lists():
	q = {
		"aggs": {
			"Artist": {
				"terms": {
					"field": "artist_si.keyword",
					"size": 100000
				}
			},
			"Music": {
				"terms": {
					"field": "music_si.keyword",
					"size": 1000000
				}
			},
			"Lyricist": {
				"terms": {
					"field": "lyricist_si.keyword",
					"size": 1000000
				}
			},
			"Melody": {
				"terms": {
					"field": "melody_si.keyword",
					"size": 1000000
				}
			}
		}

	}

	return q

def multi_match(query, fields=['title_si','artist_si','lyrics'], operator ='or'):
	q = {
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness": "AUTO"
			}
		}
	}

	q = json.dumps(q)
	return q

def multi_match_filtered(query, filters, fields=['lyrics'], operator ='or'):
	q = {
		"query": {
			"bool":{
				"should":{
					"multi_match": {
						"query": query,
						"fields": fields,
						"operator": operator,
						"type": "best_fields"
					}
				},
				"must":{
					"match" : {
						
					}
				}
			}	
		}
	}

	q["query"]["bool"]["must"]["match"] = filters

	q = json.dumps(q)
	return q

def agg_multi_match(query, fields=['title_si','lyrics'], operator ='or'):
	q = {
		"size": 500,
		"explain": True,
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness": "AUTO"
			}
		},
		"aggs": {
			"Artist Filter": {
				"terms": {
					"field": "artist_si.keyword",
					"size": 10
				}
			},
			"Music Filter": {
				"terms": {
					"field": "music_si.keyword",
					"size": 10
				}
			},
			"Lyricist Filter": {
				"terms": {
					"field": "lyricist_si.keyword",
					"size": 10
				}
			},
			"Melody Filter": {
				"terms": {
					"field": "melody_si.keyword",
					"size": 10
				}
			}
		}
	}

	q = json.dumps(q)
	return q

def multi_match_best(query, sort_num, fields=['artist_si','artist_en'], operator ='or'):
	q = {
		"size": sort_num,
		"sort": [
			{"views": {"order": "desc"}},
		],
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness": "AUTO"
			}
		}
	}

	q = json.dumps(q)
	return q

def agg_multi_match_best(query, sort_num, fields=['artist_si'], operator ='or'):
	q = {
		"size": sort_num,
		"sort": [
			{"views": {"order": "desc"}},
		],
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness": "AUTO"
			}
		},
		"aggs": {
			"Artist Filter": {
				"terms": {
					"field": "artist_si.keyword",
					"size": 10
				}
			},
			"Music Filter": {
				"terms": {
					"field": "music_si.keyword",
					"size": 10
				}
			},
			"Lyricist Filter": {
				"terms": {
					"field": "lyricist_si.keyword",
					"size": 10
				}
			},
			"Melody Filter": {
				"terms": {
					"field": "melody_si.keyword",
					"size": 10
				}
			}
		}
	}
	q = json.dumps(q)
	return q

def filter_q(query, filters, fields=['lyrics'], operator ='or'):
	q = {
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness": "AUTO"
			}
		}
	}

	q["filter"]["term"] = filters

	q = json.dumps(q)
	return q