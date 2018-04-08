.PHONY: clean install

clean:
	@rm clop.egg-info dist build -rf
install:
	@python setup.py install
