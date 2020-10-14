PeggleDeluxe = Peggle\ Deluxe
PeggleNightsDeluxe = Peggle\ Nights\ Deluxe
PNG = png

CONVERT_EXEC = python3/main.py

.PHONY: all
all:
	time python3 $(CONVERT_EXEC) --input-dir $(PeggleDeluxe) --output-dir $(PeggleDeluxe)/$(PNG)
	time python3 $(CONVERT_EXEC) --input-dir $(PeggleNightsDeluxe) --output-dir $(PeggleNightsDeluxe)/$(PNG)

.PHONY: clean
clean:
	-rm -rfv $(PeggleDeluxe)/$(PNG)/* $(PeggleNightsDeluxe)/$(PNG)/*