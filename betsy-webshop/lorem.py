import random

lorem_s = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. ','Proin aliquam justo sed ligula vehicula vulputate nec ut neque. ','Praesent eu odio malesuada, tempor ante sit amet, consequat lectus. ', 'Mauris ac tortor ut elit congue porta. ', 'Vestibulum ornare tortor sit amet cursus tincidunt. ', 'Nulla sed sapien vulputate, pretium orci sit amet, porta enim. ', 'Donec vehicula nunc et neque scelerisque, sit amet posuere ligula feugiat. ', 'Vestibulum mollis est vel tellus rutrum, eget malesuada nulla semper.', 'Etiam laoreet est placerat nulla pharetra, in pretium enim imperdiet. ', 'Suspendisse non turpis vitae libero gravida fringilla quis eget orci. ' ,'Aliquam fringilla nibh non posuere pretium. ', 'Fusce vulputate lectus molestie, elementum elit imperdiet, laoreet ligula. ', 'Proin a nibh accumsan, bibendum eros a, ullamcorper turpis. ', 'Ut euismod massa in ligula elementum facilisis ac hendrerit elit. ', 'Donec ultricies nibh commodo sodales tempus. ', 'Etiam tincidunt eros in nisi tempus, eu dignissim libero finibus. ', 'Fusce dignissim enim nec elit aliquam, id viverra massa auctor. ', 'Aliquam ullamcorper justo placerat faucibus fringilla. ' ]

def lorem_i(number):
    return random.sample(lorem_s, number)