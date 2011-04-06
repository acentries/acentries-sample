#!/usr/bin/ruby


def check_printer_state()
  ret = {}
  ret['current_ip']      = "#{ /IPv4 Settings:\s+Address:\s+([\w\.]+)/.match(`nm-tool`).to_a[1] }"
  ret['name']            = "#{ `uname -nr`.chomp } のプリンタ"
  ret['printer_state']   = `lpstat -p`.gsub("\n","<br>")
  ret['scanner_state']   = `scanimage -L`.split(/[\r\n]+/).collect{|value| /device\s+`[^']+' is a (.+)/.match(value).to_a[1] }.compact.join("<br>")

  File.open("state.log","w"){|f|
    f.puts "{"
    ret.each_pair{|key,value|  f.puts "'#{key}' : '#{value}'," }
    f.print "}"
  }
  return ret
end

def daemon_reset(name)
  {
    "printer" => proc{ system "/etc/init.d/cups restart" },
    "scanner" => proc{ system "/etc/init.d/xinetd restart" }
  }.fetch(name,proc{}).call
end


reset = ARGV[0]

if( (File.mtime("state.log") + 5) < Time.now)

fork{
  ENV["LANG"] = "ja_JP.UFT-8"
  if reset
    daemon_reset( reset )
  end
  check_printer_state
}
end

