class CreateBids < ActiveRecord::Migration[5.1]
  def change
    create_table :bids do |t|
      t.string :bidder
      t.float :amount

      t.timestamps
    end
  end
end
