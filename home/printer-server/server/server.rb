

require 'webrick'
require 'webrick/httpproxy'


def check_printer_state()
  ret = {}
  ret['current_ip']      = "#{ /IPv4 Settings:\s+Address:\s+([\w\.]+)/.match(`nm-tool`).to_a[1] }"
  ret['name']            = "#{ `uname -nr`.chomp } のプリンタ"
  ret['default_printer'] = `lpstat -d`.split(":")[1].chomp
  ret['printer_state']   = `lpstat -p`.gsub("\n","<br>")
  #ret['scanner_state']   = `scanimage -L`.gsub("\n","<br>")

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



class HelloServlet < WEBrick::HTTPServlet::AbstractServlet
  def do_GET(req,res)
    callback = req.query["callback"]
    restart  = req.query["restart"]

    if restart
      daemon_reset(restart)
    end
    check_printer_state()

    res['Content-Type'] = "application/json"
    res.body = callback + "(#{ File.read('state.log') })"
  end

end


serv = WEBrick::HTTPServer.new({:Port => 10080})
trap('INT'){ serv.shutdown }


serv.mount("/printer",WEBrick::HTTPServlet::FileHandler,'')
serv.mount("/printer_state",HelloServlet,'')

serv.start
