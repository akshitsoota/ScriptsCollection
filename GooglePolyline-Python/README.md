## Google's Encoded Polyline Algorithm Format Encoder and Decoder

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

Assuming all the files in this folder have been imported:

To encode a latitude-longitude pair, say: `(38.5, -120.2)`, make the following call:

```python
PolylineEncoder().convertLatLngPair(38.5, -120.2)
```

The results can be confirmed at [this link](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)

To encode multiple LatLng pairs, say: `(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)`, make the following call:

```python
PolylineEncoder().findPolyline([(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)])
```

Similarly, to decode the string `_p~iF~ps|U`, run the following:

```python
PolylineDecoder().convertToArrayOfLatLngPoints("_p~iF~ps|U")
```

And to decode the string <code>_p~iF~ps|U_ulLnnqC_mqNvxq`@</code>, run the following:

```python
PolylineDecoder().convertToArrayOfLatLngPoints("_p~iF~ps|U_ulLnnqC_mqNvxq`@")
```
