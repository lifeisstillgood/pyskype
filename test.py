import pyskype
import cmd

class myskype(cmd.Cmd):
    """Simple command processor example."""

    def preloop(self):
        self.p = pyskype.pySkype()
        try:
            self.p.start()
        except (KeyboardInterrupt, SystemExit):
            self.p.close()
            sys.exit()

    
    def do_call(self, line):
        self.p.invoke('CALL %s' % line)
    
if __name__ == '__main__':
    myskype().cmdloop()




