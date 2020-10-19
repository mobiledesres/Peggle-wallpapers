PeggleDeluxe := Peggle\ Deluxe
PeggleNightsDeluxe := Peggle\ Nights\ Deluxe
PNG := png

CONVERT_EXEC = python3/main.py

define CONVERT_DIRS
python3 $(CONVERT_EXEC) --input-dir $(1) --output-dir $(2)
endef

.PHONY: all
all:
	$(call CONVERT_DIRS,$(PeggleDeluxe),$(PeggleDeluxe)/$(PNG))
	$(call CONVERT_DIRS,$(PeggleNightsDeluxe),$(PeggleNightsDeluxe)/$(PNG))

.PHONY: clean
clean:
	-rm -rfv $(PeggleDeluxe)/$(PNG)/* $(PeggleNightsDeluxe)/$(PNG)/*