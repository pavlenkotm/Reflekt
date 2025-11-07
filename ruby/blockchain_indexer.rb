#!/usr/bin/env ruby
# frozen_string_literal: true

require 'net/http'
require 'json'
require 'uri'

##
# BlockchainIndexer - Ruby tool for indexing blockchain data
# Demonstrates Ruby patterns for Web3 data analysis
#
class BlockchainIndexer
  attr_reader :rpc_url, :chain_id

  def initialize(rpc_url = 'https://eth.llamarpc.com')
    @rpc_url = rpc_url
    @request_id = 0
    @chain_id = fetch_chain_id
    puts "✅ Connected to chain ID: #{@chain_id}"
  end

  ##
  # Make JSON-RPC call to blockchain
  #
  def rpc_call(method, params = [])
    @request_id += 1

    uri = URI.parse(@rpc_url)
    request = Net::HTTP::Post.new(uri)
    request.content_type = 'application/json'
    request.body = JSON.dump({
      jsonrpc: '2.0',
      method: method,
      params: params,
      id: @request_id
    })

    response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == 'https') do |http|
      http.request(request)
    end

    result = JSON.parse(response.body)
    raise "RPC Error: #{result['error']}" if result['error']

    result['result']
  end

  ##
  # Get current block number
  #
  def current_block
    block_hex = rpc_call('eth_blockNumber')
    block_hex.to_i(16)
  end

  ##
  # Get block by number
  #
  def get_block(block_number)
    hex_block = format('0x%x', block_number)
    rpc_call('eth_getBlockByNumber', [hex_block, true])
  end

  ##
  # Get balance of address
  #
  def get_balance(address)
    balance_wei = rpc_call('eth_getBalance', [address, 'latest'])
    wei_to_ether(balance_wei.to_i(16))
  end

  ##
  # Get transaction by hash
  #
  def get_transaction(tx_hash)
    rpc_call('eth_getTransactionByHash', [tx_hash])
  end

  ##
  # Index recent blocks
  #
  def index_blocks(count = 10)
    current = current_block
    blocks = []

    puts "\n📦 Indexing last #{count} blocks..."

    count.times do |i|
      block_num = current - i
      block = get_block(block_num)

      blocks << {
        number: block_num,
        hash: block['hash'],
        timestamp: block['timestamp'].to_i(16),
        tx_count: block['transactions'].length,
        gas_used: block['gasUsed'].to_i(16)
      }

      print '.'
    end

    puts "\n"
    blocks
  end

  ##
  # Analyze block statistics
  #
  def analyze_blocks(blocks)
    total_txs = blocks.sum { |b| b[:tx_count] }
    total_gas = blocks.sum { |b| b[:gas_used] }
    avg_txs = total_txs / blocks.length
    avg_gas = total_gas / blocks.length

    {
      total_blocks: blocks.length,
      total_transactions: total_txs,
      average_transactions: avg_txs,
      total_gas_used: total_gas,
      average_gas_used: avg_gas
    }
  end

  private

  def fetch_chain_id
    chain_hex = rpc_call('eth_chainId')
    chain_hex.to_i(16)
  end

  def wei_to_ether(wei)
    (wei / 10**18.0).round(6)
  end
end

##
# Example usage
#
if __FILE__ == $PROGRAM_NAME
  puts '🔍 Ruby Blockchain Indexer'
  puts '=' * 40

  indexer = BlockchainIndexer.new

  # Get current block
  puts "\n1️⃣  Current block: #{indexer.current_block}"

  # Check Vitalik's balance
  vitalik = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
  balance = indexer.get_balance(vitalik)
  puts "2️⃣  Vitalik's balance: #{balance} ETH"

  # Index recent blocks
  blocks = indexer.index_blocks(5)

  # Analyze
  stats = indexer.analyze_blocks(blocks)
  puts "\n📊 Block Statistics:"
  puts "   Total transactions: #{stats[:total_transactions]}"
  puts "   Average per block: #{stats[:average_transactions]}"
  puts "   Total gas used: #{stats[:total_gas_used]}"

  puts "\n✅ Indexing complete!"
end
