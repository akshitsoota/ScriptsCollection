'''

AUTHOR:
    Akshit (Axe) Soota

VERSION: 1.0

Class to convert a list of LatLng pairs into Encoded Polyline Algorithm Format
Steps follow the guide at:
  https://developers.google.com/maps/documentation/utilities/polylinealgorithm

'''

class PolylineEncoder:

    def twosComplement(self, number):
        if number < 0:
            return "{0:032b}".format((1 << 32) + number)
        return number

    def numberToBinary(self, number):
        if number < 0:
            number = abs(number)
        return "{0:032b}".format(number)

    def roundNumberToCorrectFormat(self, number):
        return int(round(number * pow(10, 5), 0))

    def chunks(self, list, length):
        # CITATION: http://stackoverflow.com/a/312464
        return [list[i:i+length] for i in xrange(0, len(list), length)]

    def invert(self, string):
        return ''.join(["0" if ch == "1" else "1" for ch in string])

    def convertPointToEncoding(self, point):
        formatted = self.roundNumberToCorrectFormat(point)
        if formatted < 0:
            formatted = self.twosComplement(formatted)
        else:
            formatted = self.numberToBinary(formatted)
        # Left-shift
        formatted = formatted[1:] + "0"
        # Invert if necessary
        if point < 0:
            formatted = self.invert(formatted)
        # Chunkify it
        formatted = self.chunks(formatted[::-1], 5)[::-1]
        #while not len(formatted[0]) == 5:
            #formatted = formatted[1:]
        formatted = map(lambda item: item[::-1], formatted)
        formatted = formatted[::-1]
        while formatted[-1] == "0" * len(formatted[-1]):
            formatted = formatted[:-1]
        # formatted = filter(lambda chunk: chunk != "00000", formatted)
        # Or with 0x20
        last_chunk = formatted[-1]
        formatted = [(int("0b" + chunk, 2) | 0x20) for chunk in formatted[:-1]]
        formatted.append(int("0b" + last_chunk, 2))
        # Add 63 to each and make them characters
        formatted = ''.join(map(lambda num: chr(num + 63), formatted))
        # Return
        return formatted

    def convertLatLngPair(self, lat, lng):
        return ''.join([self.convertPointToEncoding(lat), self.convertPointToEncoding(lng)])

    def findPolyline(self, lst):
        if len(lst) == 0:
            return ""
        # Else
        str = self.convertLatLngPair(lst[0][0], lst[0][1])
        for idx in range(1, len(lst)):
            str += self.convertLatLngPair(lst[idx][0] - lst[idx - 1][0], lst[idx][1] - lst[idx - 1][1])
        return str

# Inline assertion tests
assert PolylineEncoder().findPolyline([(38.5, -120.2)]) == "_p~iF~ps|U"
assert PolylineEncoder().findPolyline([(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]) == "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
