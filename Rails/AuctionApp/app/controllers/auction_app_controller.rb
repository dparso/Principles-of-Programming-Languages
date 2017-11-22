class AuctionAppController < ApplicationController
  def index
  	puts "------------ In Index ------------"
  	@allBids = Bid.all
  	puts "# of bids = #{@allBids.size}"
  	@allBids = @allBids.sort_by {|bid| [-bid.amount, bid.bidder]}

  end

  def enterBid
  	puts "------------ In Enter Bid ------------"
  	bidder = params[:bidderInput]
  	amount = params[:amountInput].to_f
  	map = {"bidder" => bidder, "amount" => amount}
  	newRow = Bid.new(map)
  	respond_to do |format|
  		if newRow.save
  			puts "Success!"
  			format.html {redirect_to auction_app_url}
  		else
  			format.html {redirect_to "/"}
  		end
  	end
  end
end
