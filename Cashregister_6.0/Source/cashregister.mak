SRCS = Cashregister.c Main.c Productdatabase.c Specialoffer.c Userinterface.c 
OBJS = Cashregister.o Main.o Productdatabase.o Specialoffer.o Userinterface.o 
DEPS = Cashregister.d Main.d Productdatabase.d Specialoffer.d Userinterface.d 

ifdef ComSpec
	RM = del
else
	RM = rm
endif

all: Cashregister.exe

Cashregister.exe: $(OBJS)
	@echo 'Building target: $@'
	gcc -o Cashregister.exe $(OBJS)
	@echo 'Finished building target: $@'
	@echo ' '

clean:
	$(RM) $(OBJS) $(DEPS) *.exh Cashregister.exe


%.o: %.c
	@echo 'Building file: $<'
	gcc -O0 -g3 -W -I. -DMinGW -DTUTORIAL -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
