keyStrBase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
keyStrUriSafe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$"
baseReverseDic = {'+': 62, '/': 63, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56, '7': 59, '6': 58, '9': 61, '8': 60, '=': 64, 'A': 0, 'C': 2, 'B': 1, 'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9, 'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18, 'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23, 'Z': 25, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29, 'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38, 'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43, 'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51}

#import sys
#baseReverseDic = {}
#alphabet = keyStrBase64
#for i in range(len(alphabet)):
#  baseReverseDic[alphabet[i]] = i
#print baseReverseDic
#sys.exit()

def decompressFromBase64(input):
  if input == None:
    return ''
  if input == '':
    return ''
  return lzdecompress(len(input), 32, input)

def one_if_greater_than_zero(val):
  if val > 0:
    return 1
  return 0

def assign_array(arr, idx, val):
  while len(arr) < idx+1:
    arr.append(0)
  arr[idx] = val

def lzdecompress(length, resetValue, input):
  dictionary = []
  next = 0
  enlargeIn = 4
  dictSize = 4
  numBits = 3
  entry = ''
  result = []
  i = 0
  w = 0
  bits = 0
  resb = 0
  maxpower = 0
  power = 0
  c = 0
  data = {
    'val': baseReverseDic[input[0]],
    'position': resetValue,
    'index': 1
  }
  for i in range(3):
    assign_array(dictionary, i, i)
  bits = 0
  maxpower = pow(2, 2)
  power = 1
  while power != maxpower:
    resb = data['val'] & data['position']
    data['position'] >>= 1
    if data['position'] == 0:
      data['position'] = resetValue
      data['val'] = baseReverseDic[input[data['index']]]
      data['index'] += 1
    bits |= one_if_greater_than_zero(resb) * power
    power <<= 1
  
  next = bits
  if next == 0:
    bits = 0
    maxpower = pow(2, 8)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = baseReverseDic[input[data['index']]]
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    c = unichr(bits)
  elif next == 1:
    bits = 0
    maxpower = pow(2, 16)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = baseReverseDic[input[data['index']]]
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    c = unichr(bits)
  elif next == 2:
    return ''
  
  assign_array(dictionary, 3, c)
  w = c
  result.append(c)
  while True:
    if data['index'] > length:
      return ''
    bits = 0
    maxpower = pow(2, numBits)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = baseReverseDic[input[data['index']]]
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    
    c = bits
    old_c = c
    if old_c == 0:
      bits = 0
      maxpower = pow(2, 8)
      power = 1
      while power != maxpower:
        resb = data['val'] & data['position']
        data['position'] >>= 1
        if data['position'] == 0:
          data['position'] = resetValue
          data['val'] = baseReverseDic[input[data['index']]]
          data['index'] += 1
        bits |= one_if_greater_than_zero(resb) * power
        power <<= 1
      assign_array(dictionary, dictSize, unichr(bits))
      dictSize += 1
      c = dictSize - 1
      enlargeIn -= 1
    elif old_c == 1:
      bits = 0
      maxpower = pow(2, 16)
      power = 1
      while power != maxpower:
        resb = data['val'] & data['position']
        data['position'] >>= 1
        if data['position'] == 0:
          data['position'] = resetValue
          data['val'] = baseReverseDic[input[data['index']]]
          data['index'] += 1
        bits |= one_if_greater_than_zero(resb) * power
        power <<= 1
      assign_array(dictionary, dictSize, unichr(bits))
      dictSize += 1
      c = dictSize - 1
      enlargeIn -= 1
    elif old_c == 2:
      return ''.join(result)
    
    if enlargeIn == 0:
      enlargeIn = pow(2, numBits)
      numBits += 1
    
    if len(dictionary) > c and dictionary[c]:
      entry = dictionary[c]
    else:
      if c == dictSize:
        entry = w + w[0]
      else:
        return ''
    result.append(entry)
    
    assign_array(dictionary, dictSize, w + entry[0])
    dictSize += 1
    enlargeIn -= 1
    
    w = entry
    
    if enlargeIn == 0:
      enlargeIn = pow(2, numBits)
      numBits += 1