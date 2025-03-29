
# Checklist*
 
1. For TXT record of a domain name [nslookup.io](https://nslookup.io)
2. for audio steganography [stegonaut](https://www.stegonaut.com/)
3. For whitespace trimming bypass ${IFS} or read file using cat<flag or strings<flag 
4.  wget -r -np http://test.com
   This command will recursively download all files and subdirectories from http://test.com, but it will not follow links that lead to parent directories. 

5.   ls -lart
   This command lists all files (including hidden ones) in reverse chronological order, with the oldest files appearing first and the most recently modified files at the bottom.

6.  https://github.com/Hedroed/png-parser
    For png image chunk analysis

7.  http://dialabc.com/sound/detect/index.html
    For DTMF decoder

8.  To find base64 data strings -a * | grep -E "\b\w{50,}\b"

9.  online steg tool https://georgeom.net/StegOnline

10. whitespace encoding: \t ---> 1 space ----> 0
11. https://330k.github.io/misc_tools/unicode_steganography.html for decoding zero width encoding
12. Request bin works same as like ngrok
13. .git/logs/refs/heads/master
14. https://github.com/spaze/hashes/blob/master/md5.md 
    For php type juggling hash comparison
15. Dont forget to increase the image height and width in stego
16. 
```bash
  stegsnow -C -p "yourpassword" output.txt
```
To extract hidden data within whitespace characters(tab/space)

17. different version of localhost
   0.0.0.0/0/0x/0x0.0x0.0x0.0x0  
   127.1  
   127.000000000000*1  
   in octal representation   
   in hex representation  

18. try xoring with image in steganography
19. to mount a file system
```bash
       mkdir mountpoint; sudo mount d mountpoint
```
20. https://fotoforensics.com/
21. http://google.com/url?q=http://example.com/  open redirection using google.com(half open redirection needs user interaction)
23. https://siunam321.github.io/ctf/ check this out
24.
```bash 
stepic --decode --image-in PNG_Magic.png --out new_image.png
```
25. to extract usb transferred file "packets having size greater than 1000 bytes with flags URB_BULK out/in"

26.
?tom[]=1&jerry[]=2  
When you pass arrays as parameters:

$_GET['tom'] != $_GET['jerry'] will be true because they are different arrays
When PHP tries to concatenate 'ACECTF' with these arrays, it converts the arrays to strings, resulting in 'ACECTFArray' in both cases
Since md5('ACECTFArray') == md5('ACECTFArray'), the second condition is satisfied

27. dont just rely on browser make curllllllll!!
28. to fix broken video fix.video
29. GIF89a; is the gif file header useful for bypassing file upload restriction
30. ezzip to find frames from a gif file