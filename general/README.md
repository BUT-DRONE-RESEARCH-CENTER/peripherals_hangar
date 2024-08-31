# Peripherals Server Integration
## Execution
- when ran with the argument --landing_pad or -lp the script will account only for the peripherals present on the landing pad (meaning only one of two cameras)

## Known Issues
- cameras cannot provide live feed to server, because stream server has to be set up on rpi (or it has to be solved via other methods)
- correct server url is not known in the script
- this version of the script has not been tested, scripts have **been only tested separately**
- pins for checking whether landing pad is connected have not been dedicated yet and connectors have not been implemented mechanically
