load "open-uri.rb"

url = "http://www.bowdoin.edu"
begin
	webPage = open(url).read
	puts webPage.class
	puts "Here goes"
	webPage.each_line do |line|
		print line
	end
rescue
	puts "Error: "
	puts "\t#{$!}"
end
puts "\nEnd!"