Rails.application.routes.draw do
  get 'auction_app/index'
  root "auction_app#index"
  get "auction_app" => "auction_app#index"
  get "/" => "auction_app#index"
  post "/" => "auction_app#enterBid"


  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
