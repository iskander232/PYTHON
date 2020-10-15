#  1ое ревью в рамках курса по Python

#  Что это

Программа, которая шифрует/дешифрует тексты на латинице различными шифрами. 
Шифрование оставляет нетронутыми знаки препинания, пробелы и переносы строк, заглавные буквы переводит в заглавные и наоборот. 

## Шифрование

./encryptor.py encode --cipher {caesar,vigenere} --key {number|word} [--input-file input.txt] [--output-file output.txt]
Зашифровать входное сообщение. 
Аргументы: 
  --cipher - тип шифра: caesar (Шифр Цезаря) или vigenere (Шифр Виженера). 
  --key - ключ шифра. Для шифра Цезаря - число, соответствующее сдвигу, для шифра Виженера - слово, которое задает сдвиги.
  --input-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, текст вводится с клавиатуры.
  --output-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, текст выводится в консоль.

## Дешифрование

./encryptor.py decode --cipher [caesar,vigenere] --key {number for caesar or word for vigenere} [--input-file input.txt] [--output-file output.txt]
Расшифровать входное сообщение, зная шифр и ключ, с которым оно было зашифровано. 
Аргументы: 
  --cipher - тип шифра: caesar (Шифр Цезаря) или vigenere (Шифр Виженера). 
  --key - ключ шифра. Для шифра Цезаря - число, соответствующее сдвигу, для шифра Виженера - слово, которое задает сдвиги.
  --input-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, текст вводится с клавиатуры.
  --output-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, расшифрованное сообщение выводится в консоль.
  
## Взлом

### Идея

Безусловно, дешифровать сообщение с известным алгоритмом и ключом шифрования - это полезно. Но гораздо веселее расшифровывать сообщения без этих знаний. 
Будем расшифровывать шифр Цезаря без знания сдвига. Если бы мы расшифровывали сообщение “руками”, то мы бы могли просто выписать все варианты дешифрования (благо, вариантов сдвига не так много - всего 26), посмотреть глазами, и выбрать, какой из них выглядит как настоящий текст. Компьютер же не знает, что такое “как настоящий текст”, поэтому мы его обучим - построим простейшую языковую модель. 
Примером простейшей модели может быть частотность символов.
Идея. Скормим программе какой-нибудь достаточно большой текст (например, сонеты Шекспира) и посмотрим на распределение различных букв. 
Теперь вернемся к нашей попытке подобрать параметр сдвига. Для всех вариантов сдвига посчитаем частоты символов в варианте расшифровки для этого сдвига. Какие-то гистограммы больше похожи на “правильную”, какие-то меньше. Та, которая больше всего похожа на “правильную”, скорее всего и будет соответствовать искомому сдвигу.


### Команды
Команды для обучения и взлома имеют следующий вид:
./encryptor.py train --text-file {input.txt} --model-file {model}
Проанализировать текст и построить языковую модель 
Аргументы:
--text-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, текст вводится с клавиатуры.
--model-file - путь к файлу модели, куда будет записана вся та статистика, которую вы собрали по тексту. 

./encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file {model}
Попытаться расшифровать текст. 
Аргументы:
--input-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, текст вводится с клавиатуры.
--output-file (необязательный аргумент) - путь ко входному файлу с текстом. Если не указан, расшифрованное сообщение выводится в консоль.
--model-file - путь к файлу модели, которая будет использоваться.

