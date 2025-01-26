module ibt::IBT {
    use sui::coin::{Coin, TreasuryCap};
    use sui::transfer::{Transfer};

    struct IBT has key, store {
        owner: address,
        treasury: TreasuryCap<IBT>,
    }

    public fun initialize(owner: address): IBT {
        let treasury = TreasuryCap::new<IBT>();
        IBT { owner, treasury }
    }

    public fun mint(ibt: &mut IBT, recipient: address, amount: u64) {
        assert!(ibt.owner == signer::address_of(recipient), "Only owner can mint");
        Coin::mint(ibt.treasury, recipient, amount);
    }

    public fun burn(ibt: &mut IBT, sender: address, amount: u64) {
        assert!(ibt.owner == signer::address_of(sender), "Only owner can burn");
        Coin::burn(ibt.treasury, sender, amount);
    }
}
