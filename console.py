#!/usr/bin/python3
"""Main Console for Airbnb project"""

import cmd
import re
import sys
import json
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """exits the program"""
        return True

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_EOF(self, arg):
        """end or exit the program"""
        return True

    def help_quit(self):
        print("command to exit the program")
        print(" ")

    def emptyline(self):
        pass

    def run_command(self, command):
        self.onecmd(command)

    def check_class(self, class_name):
        classes = ["BaseModel"]
        return class_name in classes

    def do_create(self, args):
        if not args:
            print("** class name missing **")
            return

        class_name = args.split()[0]

        if not self.check_class(class_name):
            print("** class doesn't exist **")
            return

        new_instance = BaseModel()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        if len(args_list) < 2:
            print("** instance id missing **")
            return

        class_name = args_list[0]
        instance_id = args_list[1]

        if not self.check_class(class_name):
            print("** class doesn't exist **")
            return

        all_instances = storage.all()
        key = "{}.{}".format(class_name, instance_id)
        instance = all_instances.get(key, None)
        if instance:
            print(instance)
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        if not args:
            print("** class name missing **")
            return

        arg_list = args.split()
        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        class_name = arg_list[0]
        instance_id = arg_list[1]

        if not self.check_class(class_name):
            print("** class doesn't exist **")
            return

        all_instances = storage.all()
        key = "{}.{}".format(class_name, instance_id)
        instance = all_instances.get(key, None)
        if instance:
            del all_instances[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        class_name = args.split()[0] if args else None

        if class_name and not self.check_class(class_name):
            print("** class doesn't exist **")
            return

        all_instances = storage.all()
        instances = []
        for key, instance in all_instances.items():
            if class_name is None or key.startswith(class_name):
                instances.append(str(instance))
        print(instances)

    def do_update(self, args):
        args_list = args.split()

        if not args:
            print("** class name missing **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return

        if len(args_list) < 4:
            print("** value missing **")
            return

        class_name = args_list[0]
        instance_id = args_list[1]
        attribute_name = args_list[2]
        attribute_value = args_list[3]

        if not self.check_class(class_name):
            print("** classs doesn't exist **")
            return

        all_instances = storage.all()
        key = "{}.{}".format(class_name, instance_id)
        instance = all_instances.get(key, None)

        if instance:
            try:
                atttribute_value = eval(attribute_value)
            except (NameError, SyntaxError):
                pass

            setattr(instance, attribute_name, attribute_value)
            instance.save()
        else:
            print("** no instance found **")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        commands = " ".join(sys.argv[1:])
        HBNBCommand().run_command(commands)
    else:
        if sys.stdin.isatty():
            HBNBCommand().cmdloop()
        else:
            for line in sys.stdin:
                HBNBCommand().run_command(line.strip())
