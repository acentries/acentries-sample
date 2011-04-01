#!/usr/bin/ruby

require "cgi"

def check_printer_state()
  ret = {}
  ret['current_ip']      = "#{ /IPv4 Settings:\s+Address:\s+([\w\.]+)/.match(`nm-tool`).to_a[1] }"
  ret['name']            = "#{ `uname -nr`.chomp } のプリンタ"
  #ret['default_printer'] = `lpstat -d`.split(":")[1].chomp
  ret['printer_state']   = `lpstat -p`.gsub("\n","<br>")
  #ret['scanner_state']   = `scanimage -L`.split("\n").collect{|value| /device\s+`([^']+)'/.match(value).to_a[1] }.compact.join("<br>")

  File.open("state.log","w"){|f|
    f.write "{\n"
    ret.each_pair{|key,value|
      f.write "'#{key}' : '#{value}',\n"
    }
    f.write "}"
  }
  return ret
end

def daemon_reset(name)
  {
    "printer" => proc{ system "/etc/init.d/cups restart" },
    "scanner" => proc{ system "/etc/init.d/xinetd restart" }
  }.fetch(name,proc{}).call
end



cgi = CGI.new

callback = cgi["callback"]
restart  = cgi["restart"]

system "ruby update-daemon.rb #{restart}"

print "Content-Type: application/json;charset=utf-8\n\n"
print callback + "(#{ File.read('state.log') })"
