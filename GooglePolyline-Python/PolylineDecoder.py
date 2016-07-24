'''

AUTHOR:
    Akshit (Axe) Soota

VERSION: 1.0

Class to convert a string in the Encoded Polyline Algorithm Format back to a list of LatLng points
Steps reversed from the guide at:
  https://developers.google.com/maps/documentation/utilities/polylinealgorithm

'''

class PolylineDecoder:

    # CITATION: http://stackoverflow.com/a/5833119
    def rshift(self, val, n):
        return (val % 0x100000000) >> n

    def convertToArrayOfLatLngPoints(self, string):
        # Java Code ported over to Python from: http://stackoverflow.com/a/9341670
        values = []
        truck, carriage_q = 0, 0
        for char in string:
            val = self.rshift((ord(char) - 63) << 27, 27)
            truck |= val << carriage_q
            carriage_q += 5
            if ((ord(char) - 63) & (1 << 5)) == 0:
                is_negative = ((truck & 1) == 1)
                truck = self.rshift(truck, 1)
                if is_negative:
                    truck = ~truck
                values.append(truck)
                truck, carriage_q = 0, 0
        # Now calculate differences if any
        for idx in range(2, len(values)):
            values[idx] += values[idx - 2]
        # Divide by 1E5
        values = map(lambda num: num / float(pow(10, 5)), values)
        values = [round(num, 5) for num in values]
        # Convert to tuples and return
        return [(values[idx], values[idx + 1]) for idx in range(0, len(values), 2)]

# Inline assertion tests
assert PolylineDecoder().convertToArrayOfLatLngPoints("_p~iF~ps|U") == [(38.5, -120.2)]
assert PolylineDecoder().convertToArrayOfLatLngPoints("_p~iF~ps|U_ulLnnqC_mqNvxq`@") == [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]