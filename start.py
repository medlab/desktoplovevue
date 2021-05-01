import os
import time
import webview
import logging
import threading

class Api():
    def addItem(self, title):
        print('Added item %s' % title)

    def removeItem(self, item):
        print('Removed item %s' % item)

    def editItem(self, item):
        print('Edited item %s' % item)

    def toggleItem(self, item):
        print('Toggled item %s' % item)

    def toggleFullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def cppyyDemo(self, msg):
        #--begin-- cppyy test region begion
        import cppyy

        cppyy.cppdef("""
        class MyClass {
        public:
            MyClass(int i) : m_data(i) {}
            virtual ~MyClass() {}
            virtual int add_int(int i) { return m_data + i; }
            int m_data;
        };""")

        from cppyy.gbl import MyClass

        c=MyClass(42)

        cppyy.cppdef("""
        void say_hello(MyClass* m) {
            std::cout << "Hello, the number is: " << m->m_data << std::endl;
        }""")

        MyClass.say_hello=cppyy.gbl.say_hello

        logging.warn('hello world' * 80)
        for i in range(10):
            c.add_int(3)
            c.say_hello()

        #--end-- cppyy test region begion
        logging.warn('--begin-- to call cppyyDemo'*80+msg)
        c.say_hello()
        logging.warn('--end-- to call cppyyDemo'*80+msg)

    def errorDemo(self, seconds):
        raise Exception('face error ')
        pass

    def sleepDemo(self, seconds):
        logging.warning('--begin-- backend sleepting' + str(threading.current_thread().ident) )
        time.sleep(seconds)
        logging.warning('--end-- backend sleepting' + str(threading.current_thread().ident))    

        return threading.current_thread().ident
        pass

if __name__ == '__main__':
    api = Api()
    webview.create_window('Todos magnificos', 'assets/index.html',  js_api=api, min_size=(600, 450))

    #debug will enable right click menu
    #http_server will enable a http server, which works better than files:/ protocol
    #cef engine works better for all os
    webview.start(debug=True, http_server=True, gui='cef')