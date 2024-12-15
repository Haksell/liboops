test:
	@pytest algorithms/* classes/*

clean:
	rm -rf __pycache__ .pytest_cache .benchmarks
	rm -rf */__pycache__ */.pytest_cache */.benchmarks