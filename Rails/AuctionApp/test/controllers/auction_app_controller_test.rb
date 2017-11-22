require 'test_helper'

class AuctionAppControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get auction_app_index_url
    assert_response :success
  end

end
