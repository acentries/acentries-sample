


site_name = "printer"
site_path = "/home/ubuntu/.userdata/apatch-main-site"
old_site = File.basename(Dir['/etc/apache2/sites-enabled/*'][0].to_s)

cgi_main = "printer_state"
cgi_main_path = "printar_call.rb"
back_daemon = "update_daemon.rb"

client_main = "client.html"



Dir.mkdir("public_html")
Dir.mkdir("cgi-bin")

Dir.chdir("public_html")
File.symlink("../" + client_main, client_main)
File.symlink("/usr/share/sounds/purple/alert.wav","notify.wav")

Dir.chdir("../cgi-bin")
File.symlink("../" + cgi_main_path, cgi_main)
File.symlink("../" + back_daemon, back_daemon)


#サイトの切り替え
File.symlink(site_path,"/etc/apache2/sites-available/#{site_name}")

system "a2dissite #{old_site }"
system "a2ensite #{site_name}"