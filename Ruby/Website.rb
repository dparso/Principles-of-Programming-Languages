load "open-uri.rb"

class Website
	@@protocol = "http"
	attr_reader :url, :broken

	def initialize(url)
		@url = url
		@broken = nil
	end

	def broken?
		if @broken == nil
			begin
				content = open(@url).read
				@broken = false
			rescue
				@broken = true
			end
		else
			@broken
		end
	end

	def showInfo
		print "Is ", @url, " broken? ", broken?, "\n"
	end
end

w = Website.new("http://www.bowdoin.edu/")
w.showInfo
puts "URL: #{w.url}"


class Website
	attr_accessor :is_pdf

	def pdf?
		if @url =~ /.+\.(pdf)$/i
			@is_pdf = true
		else
			@is_pdf = false
		end
	end
end

puts "Is it pdf? #{w.pdf?}"


w2 = Website.new("http://www.bowdoin.edu/president")

def w2.president
	@president_name = "Clayton Rose"
end

puts w2.president
#w.president would return an error

class PersonalWebsite < Website
	attr_reader :owner

	def initialize(url)
		super(url)

		if url =~ /~(.+)$/i || url =~ /~(.+)\//i
			@owner = $1
		else
			@owner = nil
		end
	end
end

myWebsite = PersonalWebsite.new("http://www.bowdoin.edu/~mirfan")
puts "Owner: #{myWebsite.owner}, URL: #{myWebsite.url}"
