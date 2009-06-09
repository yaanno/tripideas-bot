# Trip Ideas
A simple Python Bot/Application for Google AppEngine to search Flight data.

## Kayak API
The good news is that Kayak API is working well with GAE

## ClearTrip API
Currently experimental

## Todo
- Kayak Hotel Search API
- Scheduling
- Twitter Request/Response API

## Usage
To start a search from twitter, send a message to @tripideas. Message format for flight search:

    @tripideas #flight MAD-LON (2009-07-10|2009-08-10)

Formally:

    @tripideas #SERVICE FROM-TO (DEPARTUREDATE-RETURNDATE) 

- SERVICE: flight or hotel
- FROM & TO: IATA codes
- DEPARTUREDATE & RETURNDATE: YYYY/MM/DD

If no RETURNDATE specified that means you request for an one way trip.

Note: Kayak API session is limited to 30-40 minutes