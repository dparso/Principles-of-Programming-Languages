class Website
	def initialize(url)
		@url = url
		@broken = false
	end
	attr_reader :url, :broken
	attr_writer :broken
end

module PersonalInformation
	@EMERGENCY_PHONE = "207-725-3500"
	@email = "no-effect@bowdoin.edu"

	attr_accessor :email

	def sendEmail
		puts "Sending to " + @email + "."
		print "Are you sure? (Y/N)"
		if gets.chomp == "Y"
			puts "Email sent"
		end
	end
end

class PersonalWebsite < Website
	include PersonalInformation

	attr_reader :owner

	def initialize(url)
		super(url)

		if url =~ /~(.+)$/i || url =~ /~(.+)\//i
			@owner = $1
			@email = "#{@owner}@bowdoin.edu"
		else
			@owner = nil
		end
	end
end

w = PersonalWebsite.new("http://www.bowdoin.edu/~some1")
puts w.owner
w.sendEmail
